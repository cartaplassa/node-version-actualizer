# node-version-actualizer
```shell
./main.sh
  date
  input path
  output path
```
You pick a date, a broken old config, script does its magic, replaces "latest" versions with major release version latest to that date. Writes the result in output.
```shell
./main.sh 21.08.2025 -i /path/to/package.json -o path/to/package.json
```

TODO:
- node.js version
- ability to pick between major release/prerelease/build
- interactive TUI
