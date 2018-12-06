# Performance Test

## Steps

### 1. Re-image or upgrade an Unity

**NOTE:** Use a physical Unity and the **RETAIL** image.

### 2. Create 2000 LUNs
```bash
$ ./create_2000_luns.sh
```

### 3. Start performance tests
```bash
./fire.sh <folder_to_put_logs>
```

### 4. Repeat #3 on different images

### 5. Generate summary informantion
```bash
./summary.sh <space_seperated_folders_where_logs_locates>
```
