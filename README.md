# Smart Education

## Usage

1. Get the code from Github clone.

   ```
   $ git clone https://github.com/zolars/SmartEdu.git
   ```

2. You need to install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) and [MySQL](http://dev.mysql.com/downloads/mysql/) on your computer.

   ```
   $ conda -V
   conda 4.8.1
   ```

   You need to set "root" as the MySQL password. Or change the password in `config.py`.

   ```
   $ mysql -u root -p
   Enter password:root
   Welcome to the MySQL monitor.  Commands end with ; or \g.
   ```

3. Create the environment.

   ```
   $ cd SmartEdu
   $ conda env create -f environment.yml
   $ conda activate smartedu
   $ python -V
   Python 3.6.8 :: Anaconda, Inc.
   ```

   If you want to update your environment, use:

   ```
   $ conda env update -f environment.yml
   ```

4. Test running flask application.

   ```
   $ conda activate smartedu
   $ export FLASK_APP=app
   $ flask run
   $ flask recreate-db
   ```

5. Deploy the nginx.

   ```
   $ cp ./config/smartedu.conf /etc/nginx/conf.d/
   $ sudo service nginx restart
   ```

6. Run the app with gunicorn.

   ```
   $ conda activate smartedu
   $ gunicorn -c ./config/gunicorn.conf.py wsgi:app
   ```

7. Server Restart.
   ```
   $ kill -9 <pid>
   $ systemctl restart mariadb.service
   $ conda activate smartedu
   $ gunicorn -c ./config/gunicorn.conf.py wsgi:app
   ```
