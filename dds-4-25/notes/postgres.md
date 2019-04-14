<link rel='stylesheet' href='markdown9.css'/>

Database roles
--------------

    postgres: SArzbxybEyLB
    dds (superuser):y8M36LkeVgGn

Databases
---------
                                      List of databases
       Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges   
    -----------+----------+----------+-------------+-------------+-----------------------
     dds       | dds      | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
     postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
     template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
               |          |          |             |             | postgres=CTc/postgres
     template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
               |          |          |             |             | postgres=CTc/postgres

WAL config
----------

    archive_mode = on
    archive_command = 'test ! -f /mnt/backup/pg_wal/%f && cp %p /mnt/backup/pg_wal/%f'
    archive_timeout = 0
    wal_level = archive