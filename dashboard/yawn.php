<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yawn</title>
</head>
<body>
    <?php 
        //Connect with database
        $con = mysqli_connect('{hostname}', '{username}', '{password}', '{database}');
        //Create query
        $query = "insert into yawns(yawn) values()";
        //Execute query
        $result = mysqli_query($con, $query);
    ?>
</body>
</html>