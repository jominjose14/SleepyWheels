<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alarm</title>
</head>
<body>
    <?php 
        //Connect with database
        $con = mysqli_connect('localhost', 'id15892287_jomin', 'phpMyAdmin85!', 'id15892287_sleepywheels');
        //Create query
        $query = "insert into alarms(alarm) values('ALARM')";
        //Execute query
        $result = mysqli_query($con, $query);
    ?>
</body>
</html>