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
    
4. Run flask application.
   ```
   $ flask clear-db
   $ flask create-db
   $ flask run
   ```