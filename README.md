Flask Test for Frappe : https://frappe.io/flask-test

- python3 -m venv env
- source env/bin/activate

## Windows

- Run in Powershell as administrator :
- Set-ExecutionPolicy unrestricted
- [Reference](https://answers.microsoft.com/en-us/windows/forum/all/execution-of-scripts-is-disabled-how-do-you-enable/e19d41b2-ab61-e011-8dfc-68b599b31bf5)

Execute `.\env\Scripts\activate.ps1` in PowerShell OR `.\env\Scripts\activate.bat` in command prompt

Install pip modules :

```sh
pip install flask
pip install flask_mysqldb
pip install pyyaml
```

## Import Database : 

```sh
Get-Content flask-test.sql | & 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe' --user=root --database=flask-test --port=3306 -p
```

## NodeJS for Development

Install [TailWindCSS + Flowbite](https://flowbite.com/docs/getting-started/flask/) :

```sh
npm install -D tailwindcss
npm install flowbite
npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch
```

![Products Index](/screenshots/product-index.jpg)

![Product Edit](/screenshots/product-edit.jpg)

Screenshots in screenshots directory

Updated to use TailWindCSS