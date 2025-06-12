# Backup

The `backup.bat` scripts uses `Restic` to backup selected directories to `S3`.

Before you run `backup.bat`, you should initialize your Restic repository. You can do this by running:
```commandline
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export RESTIC_REPOSITORY=...
export RESTIC_PASSWORD=...

restic init
```

You can then schedule it with the Windows Task Scheduler:
```commandline
backup.bat <AWS_KEY> <AWS_SECRET> <RESTIC_REPO> <RESTIC_PASSWORD> <INTERVAL_SECONDS> <PATH1> <PATH2> ...
```
