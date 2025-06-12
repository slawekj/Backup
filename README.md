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

You can then use the Windows Task Scheduler to run backups:
```commandline
backup.bat <AWS_KEY> <AWS_SECRET> <RESTIC_REPO> <RESTIC_PASSWORD> <INTERVAL_SECONDS> <PATH1> <PATH2> ...
```

The idea is to schedule this script periodically (e.g., every hour) or whenever your system is idle. I use the second
option, thus `<INTERVAL_SECONDS>` is set to `129600`. It means that the task scheduler will try to backup every time
a computer goes idle, but no sooner than 36 hours after the last backup.
