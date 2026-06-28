# Benchmark Report Format

Genesis Engine stores benchmark history in `/benchmarks/history/`. 
Each report is saved as a JSON document representing a specific compilation run.

## Monitored Metrics
- `planning_time_s`: Time spent parsing the spec and building internal rule graphs.
- `generation_time_s`: Time spent executing AST plugins and writing physical files to disk.
- `total_compilation_time_s`: Absolute wall-clock time from endpoint hit to final return.
- `peak_memory_mb`: Maximum Resident Set Size (RSS) during the compilation lifecycle.
- `cpu_time_s`: Total aggregate CPU cycles consumed across user/sys space.
- `generated_file_count`: Absolute file count written to the project workspace.
- `generated_loc`: Estimated lines of code generated.
- `bundle_size_bytes`: Compressed byte size of the final `.zip` artifact.

## Usage
Run the benchmarking suite via:
```bash
python backend/scripts/benchmark_compiler.py
```
