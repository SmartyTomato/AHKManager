# Use following command to generate exe file

```cmd
& "C:/Program Files/Python36/python.exe" -m PyInstaller "./src/ahk_manager.py" --distpath="./dist/AHK Manager" -w --onefile --icon="./resources/icon/icon.ico" --name="AHK Manager.exe" --hidden-import=PyQt5 --clean --noupx
```
