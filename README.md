## About
Go is an [open source](https://github.com/OrionBytes/TeaHouse/blob/master/LICENSE)

## How do I make an account?
You can create accounts using the provided administrator tools.py


## Build Instructions 
The backend was written in python3.5, frontend in [Vue.js](https://vuejs.org/). You will need `libpq` and `libjpeg` to get started. On linux, use
```bash
$ sudo apt-get install python3-dev libpq-dev libjpeg-dev
```

The rest of the dependencies can be installed with
- `pip install -r requirements.txt`
- `npm install`

To run the development server you will need to migrate the database. This step also needs to be run every time new DB migrations are created:
```bash
$ alembic upgrade head
```

Finally, the development server can be run with:
```bash
$ ./gulp.sh
$ ./main.py --create-room='Main Room'
```

After this the server will listen on http://localhost:8000 by default.
