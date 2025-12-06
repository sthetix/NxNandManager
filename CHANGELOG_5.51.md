# NxNandManager v5.51 - Changelog

## Major Changes

### External NCA Database Support

**Version 5.51** removes the hardcoded NCA database and now loads firmware version detection data from an external text file (`nca.txt`). This change was inspired by the [FuseCheck](https://github.com/sthetix/FuseCheck) project's approach to external database management.

## Benefits

1. **Easy Updates**: No recompilation needed when new Nintendo Switch firmware versions are released
2. **User-Friendly**: Simply edit `nca.txt` to add new firmware versions
3. **Maintainable**: NCA database is now a simple text file instead of hardcoded arrays
4. **Backward Compatible**: Falls back to internal database if `nca.txt` is not found

## What Changed

### Modified Files

- **gui/qutils.h**: Refactored `NxNcaDB` class to load from external file
- **gui/qutils.cpp**: Implemented text file parsing for NCA database
- **gui/mainwindow.cpp**: Updated to use new `NxNcaDB` constructor
- **gui/mainwindow.ui**: Updated version number to 5.51
- **NxStorage.cpp**: Refactored firmware detection to use external `nca.txt` file

### New Files

- **nca.txt**: External NCA database file with SystemVersion and ExFat NCA mappings

## NCA Database Format

The `nca.txt` file uses a simple text format:

```
[NCA] <firmware_version> <nca_filename> <title_id>
```

### Example:
```
# SystemVersion NCAs (Title ID: 0100000000000809)
[NCA] 21.0.1 e7273dd5b560d0ba282fc64206fecb56.nca 0100000000000809
[NCA] 21.0.0 4b0130c8b9d2174a6574f6247655acc0.nca 0100000000000809

# ExFat NCAs (Title ID: 010000000000081B)
[NCA] 21.0.1 5d920340732acee21eda71743688d71a.nca 010000000000081B
[NCA] 21.0.0 5d920340732acee21eda71743688d71a.nca 010000000000081B
```

### Title IDs:
- `0100000000000809`: SystemVersion (for firmware version detection)
- `010000000000081B`: BootImagePackageExFat (for exFAT driver detection)

## Updating the Database

When a new Nintendo Switch firmware is released:

1. Open `nca.txt` in a text editor
2. Add the new firmware version entries:
   ```
   [NCA] <version> <systemversion_nca> 0100000000000809
   [NCA] <version> <exfat_nca> 010000000000081B
   ```
3. Save the file
4. No recompilation needed!

## Finding NCA Filenames

You can find NCA filenames by:
1. Mounting your Nintendo Switch SYSTEM partition
2. Navigate to `/Contents/registered/` directory
3. Look for the SystemVersion NCA (Title ID 0100000000000809)
4. Look for the ExFat NCA (Title ID 010000000000081B)

## Credits

- External database approach inspired by [FuseCheck](https://github.com/sthetix/FuseCheck) by sthetix
- Original NxNandManager by [eliboa](https://github.com/eliboa/NxNandManager)

## Installation

1. Build NxNandManager v5.51 as usual
2. Place `nca.txt` in the same directory as `NxNandManager.exe`
3. Run the application

## Notes

- The application will fall back to the internal hardcoded database if `nca.txt` is not found
- Comments in `nca.txt` start with `#`
- Empty lines are ignored
- Lines must follow the exact format: `[NCA] <version> <filename> <title_id>`
