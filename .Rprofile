# Automatically include local R_libs in the library path
lib_path <- file.path(getwd(), "R_libs")
if (dir.exists(lib_path)) {
  .libPaths(c(lib_path, .libPaths()))
}
