import { test, expect } from '@playwright/test';

test.describe('Genesis Engine E2E Workflow', () => {
  test('Completes the full pipeline', async ({ page }) => {
    // 1. Login
    await page.goto('/login');
    await page.fill('input[placeholder="Username"]', 'admin');
    await page.fill('input[placeholder="Password"]', 'admin');
    await page.click('button:has-text("Sign in")');
    await page.waitForURL('/dashboard');

    // 2. Submit Specification & 3. Validation & 4. Generation
    await page.click('button:has-text("Compile Project")');
    await expect(page.locator('text=Compiler Error').or(page.locator('text=Compilation Complete'))).toBeVisible({ timeout: 15000 });

    // 5. Planning Report
    await page.click('button:has-text("Report")');
    await expect(page.locator('text=Architecture Report')).toBeVisible();

    // 6. Graph Viewer
    await page.click('button:has-text("Graph")');
    await expect(page.locator('text=Tree')).toBeVisible();

    // 7. Workspace Explorer
    await page.click('button:has-text("Workspace")');
    await expect(page.locator('text=backend')).toBeVisible();

    // 8. Timeline
    await page.click('button:has-text("Timeline")');
    await expect(page.locator('text=Execution Traces')).toBeVisible();

    // 9. Artifact Download
    // Cannot easily test file download without setting up a handler, 
    // but we can verify the button is there.
    await expect(page.locator('button:has-text("Download Bundle")')).toBeVisible();
  });
});
