# 🎉 New Features Added

## 1. Delete Case Reports ✅

### What it does:
- Allows you to delete old case reports directly from the dashboard
- Permanently removes the entire case directory and all its contents

### How to use:
1. Go to the dashboard (`http://127.0.0.1:8000`)
2. Find the case you want to delete
3. Click the red **"Delete"** button
4. Confirm the deletion in the popup dialog
5. The case will be removed and statistics will update automatically

### Features:
- ✅ Confirmation dialog to prevent accidental deletion
- ✅ Automatic refresh of dashboard after deletion
- ✅ Updates statistics immediately
- ✅ Error handling if case doesn't exist

### API Endpoint:
```
DELETE /api/case/<case_id>
```

---

## 2. File Browser for Target Selection 🗂️

### What it does:
- Provides a visual directory browser to select scan targets
- No need to manually type paths anymore!

### How to use:
1. Go to the Scan page (`http://127.0.0.1:8000/scan`)
2. Click the **"Browse"** button next to the Target Path field
3. A modal window will open showing available drives
4. Click on a drive (e.g., `C:\`, `D:\`)
5. Navigate through folders by clicking on them
6. Use the **"Up"** button to go to parent directory
7. Click **"Select This Folder"** when you find the target
8. The path will be automatically filled in the form

### Features:
- ✅ Shows all available drives on Windows
- ✅ Lists only directories (no files)
- ✅ Navigate up and down the directory tree
- ✅ Clean, scrollable interface
- ✅ Handles permission errors gracefully
- ✅ Alphabetically sorted directories

### API Endpoint:
```
GET /api/browse?path=<directory_path>
```

---

## Technical Details

### Files Modified:

1. **src/web/app.py**
   - Added `DELETE /api/case/<case_id>` endpoint
   - Added `GET /api/browse` endpoint
   - Import `shutil` for directory deletion
   - Import `os` and `string` for directory browsing

2. **src/web/templates/index.html**
   - Added delete button to each case card
   - Added `deleteCase()` JavaScript function
   - Added confirmation dialog

3. **src/web/templates/scan.html**
   - Added "Browse" button next to target path input
   - Added file browser modal dialog
   - Added JavaScript functions:
     - `loadDirectories(path)` - Load directory contents
     - `goUp()` - Navigate to parent directory
     - `selectCurrentPath()` - Select current folder

---

## Security Considerations

### Delete Feature:
- ✅ Requires user confirmation
- ✅ Validates case exists before deletion
- ✅ Logs all deletions
- ✅ Returns proper error codes

### File Browser:
- ✅ Only shows directories (not files)
- ✅ Handles permission errors
- ✅ Path validation
- ✅ No arbitrary file access
- ⚠️ **Note**: Users can only browse directories they have permission to access

---

## Usage Examples

### Delete a Case:
```javascript
// Via API
fetch('/api/case/CASE-20251013-001234', {
    method: 'DELETE'
})
.then(res => res.json())
.then(data => console.log(data.message));
```

### Browse Directories:
```javascript
// Get drives (Windows)
fetch('/api/browse')
.then(res => res.json())
.then(data => console.log(data.items));

// Browse specific directory
fetch('/api/browse?path=C:\\Users')
.then(res => res.json())
.then(data => console.log(data.items));
```

---

## Screenshots Description

### Dashboard with Delete Button:
- Each case card now has two buttons:
  - **Blue "View Report"** button
  - **Red "Delete"** button with trash icon

### File Browser Modal:
- Title: "Browse Directories"
- Current Path display with "Up" button
- Scrollable list of directories
- Each directory has a folder icon
- "Cancel" and "Select This Folder" buttons at bottom

---

## Future Enhancements

Potential improvements:
- [ ] Bulk delete (select multiple cases)
- [ ] Archive cases instead of deleting
- [ ] Restore deleted cases (recycle bin)
- [ ] File browser: Show file count in each directory
- [ ] File browser: Search functionality
- [ ] File browser: Favorites/bookmarks
- [ ] File browser: Recent paths

---

## Troubleshooting

### Delete not working:
- Check if case directory exists
- Verify file permissions
- Check browser console for errors

### File browser not loading:
- Ensure server is running
- Check for permission errors in logs
- Try refreshing the page

### Can't navigate directories:
- Some system directories may be protected
- Try a different starting point
- Check Windows permissions

---

**Enjoy the new features! 🎉**
