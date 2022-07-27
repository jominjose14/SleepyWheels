<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="dashboard.css">
    <link rel="shortcut icon" href="icon.png" type="image/x-icon">
    <title>SleepyWheels Dashboard</title>
</head>
<body>
    <?php
        //Connect with database
        $con = mysqli_connect('{hostname}', '{username}', '{password}', '{database}');
        //Create query
        $alarm_query = "select * from alarms order by timestamp desc";
        $yawn_query = "select * from yawns order by timestamp desc";
        //Execute query
        $alarm_result = mysqli_query($con, $alarm_query);
        $yawn_result = mysqli_query($con, $yawn_query);

        function month($m) {
            if($m == '01')
                return 'January';
            if($m == '02')
                return 'February';
            if($m == '03')
                return 'March';
            if($m == '04')
                return 'April';
            if($m == '05')
                return 'May';
            if($m == '06')
                return 'June';
            if($m == '07')
                return 'July';
            if($m == '08')
                return 'August';
            if($m == '09')
                return 'September';
            if($m == '10')
                return 'October';
            if($m == '11')
                return 'November';
            if($m == '12')
                return 'December';
            return 'Undefined';
        }

        function entry($timestamp) {
            echo "<div>".substr($timestamp, 0, 4)."</div>";
            echo "<div>".month(substr($timestamp, 5, 2)).' '.substr($timestamp, 8, 2)."</div>";
            echo "<div>".substr($timestamp, 11)."</div>";
        }
    ?>

    <div class="top">
        SleepyWheels
    </div>
    <div class="tables">
        <div class="head">Alarms Triggered</div>
        <div class="table">
            <div class="heading">Year</div>
            <div class="heading">Day</div>
            <div class="heading">Time</div>
            <?php
                if($alarm_result){

                    while($row = mysqli_fetch_array($alarm_result))
                    {
                        entry($row['timestamp']);
                    }
                }
            ?>
        </div>
        <br>
        <div class="head">Yawns Recorded</div>
        <div class="table">
            <div class="heading">Year</div>
            <div class="heading">Day</div>
            <div class="heading">Time</div>
            <?php
                if($yawn_result){

                    while($row = mysqli_fetch_array($yawn_result))
                    {
                        entry($row['timestamp']);
                    }
                }
            ?>
        </div>
    </div>

    <hr>

    <div class="tips">
    <div class="head">Safety Tips</div>
        <div class="tip">
            <ul>
                <li>
                    If feeling sleepy during a journey, stop somewhere safe, take drinks containing caffeine and take a short nap.
                </li>
                <li>
                    Plan the journey to include regular rest breaks (a break of at least 15 minutes at least every two hours)
                </li>
                <li>
                    Avoid setting out on a long drive after having worked a full day
                </li>
                <li>
                    Avoid driving into the period when they would normally be falling asleep
                </li>
                <li>
                    Avoid driving in the small hours (between 2am and 6am)
                </li>
            </ul>
        </div>
        <br>
        <div class="head">Exercises</div>
        <div class="tip">
            <ul>
                <li>
                    <b>Jump rope:</b> This is one of the best exercises you can do. It’s a great calorie burner, you can do it most anywhere, it strengthens muscles in your lower body and core, and it’s a lower-impact exercise than jogging. Best of all, it helps get your lymphatic system moving, which flushes waste out of your system.</li>
                <li>
                    <b>Run in place:</b> It gets your heart rate up and you can do it anywhere. If you have a treadmill nearby, feel free to use it, but if you don’t have one, don’t let that stop you from getting up to move. Running in place doesn’t replace actual running, but if you’ve got only five minutes, it could help wake you up while burning some calories.</li>
                <li>
                    <b>Perform a few burpees:</b> A “burpee” is an exercise in which you do a series of movements and end up back where you started. First, you jump straight up in the air, land and go into a squat, jump your feet back into a plank position, do one push-up, jump your feet up to your hands and move into another squat, and stand back up, ready to jump again if you can! A couple of these and you’ll be breathing hard and ready to go.</li>
                <li>
                    <b>Clean something:</b> We’re talking real cleaning here, not just reorganizing your papers. Take everything off the desk and wipe it down with a cleaning solution. If you have a home office, vacuum, or clean up the kitchen or bathroom. If you’ve got an office coffee break area, take a few minutes to make it sparkle.            </li>
                <li>
                    <b>Dance:</b> Turn on your favorite music and move as you please. Granted, this one is harder to do in a public place, but if you can get into a room where you feel safe, plug in your headphones and go for it. Bonus benefit: According to a 2003 study, frequent dancing reduced risk of dementia!            </li>
            </ul>
        </div>
    </div>
</body>
</html>