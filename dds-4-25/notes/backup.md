<link rel='stylesheet' href='markdown9.css'/>

Backup drive
------------

750 GB SATA:

    Disk /dev/sdc: 750.2 GB, 750156374016 bytes
    255 heads, 63 sectors/track, 91201 cylinders, total 1465149168 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x00000000
    
       Device Boot      Start         End      Blocks   Id  System
    /dev/sdc1              63  1465149167   732574552+  83  Linux

No hot-swap support intended presently

MongoDB backup
--------------

Advise running manually after each new census database since very few fields will be altered

    mongodump -o /mnt/backup -d censusXXXXi

Incremental filesystem backup
-----------------------------

Runs daily

    rdiff-backup /srv/ /mnt/backup/srv
    rdiff-backup /etc/ /mnt/backup/etc

Logs to syslog for review

Postgres WAL archiving
----------------------

See postgres-notes