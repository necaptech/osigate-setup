<?php
    include ('session.php');
    include('menu.php');
?>

<br />

<fieldset>
    <legend><b>Controllers Status: </b></legend><br>
    <?php
        if ($file=fopen("/srv/data/osiRele", "r")) {
            echo "<table border=1>";

            // apri connessione a db
            $connDB = mysqli_connect("localhost", "root", "root");
            if (!$connDB) {
                exit('Errore di connessione alla basedati (' . mysqli_connect_errno() . ') ' . mysqli_connect_error());
            }
            mysqli_set_charset($connDB, 'utf-8');
            mysqli_select_db($connDB, "TECNOQ");
            echo "<thead><tr><th>Controller ID</th><th>Switch No 1</th><th>Switch No 2</th>
                                                   <th>Switch No 3</th><th>Switch No 4</th>
                                                   <th>Switch No 5</th><th>Switch No 6</th>
                                                   <th>Switch No 7</th><th>Switch No 8</th>
                                                   <th>Last seen</th></tr></thead><tbody>";
            while (($id=fgets($file)) != false) {
                $id = trim($id);
                $idHex='';
                for ($i=0; $i<6; $i++){
                    $idHex .= dechex(ord($id[$i]));
                }
//                    $contrStatus = mysqli_query($connDB, "SELECT status, time FROM OSIRE_STATUS WHERE status LIKE '%" . trim($id) . "%'"
                // echo "SELECT `Status`, Unix FROM OSIRE_STATUS WHERE ReleID = '" . $id . "'" . " ORDER BY Unix DESC LIMIT 1" ;
                $contrStatus = mysqli_query($connDB, "SELECT `Status`, Unix FROM OSIRE_STATUS WHERE ReleID = '" . $id . "'" . " ORDER BY Unix DESC LIMIT 1" );
                $riga = mysqli_fetch_array($contrStatus);
                // print_r($riga);
                echo "<tr><td>" . $id . "</td><td>" . substr($riga[0], 0, 2) . "</td><td>" .
                                                      substr($riga[0], 2, 2) . "</td><td>" .
                                                      substr($riga[0], 4, 2) . "</td><td>" .
                                                      substr($riga[0], 6, 2) . "</td><td>" .
                                                      substr($riga[0], 8, 2) . "</td><td>" .
                                                      substr($riga[0], 10, 2) . "</td><td>" .
                                                      substr($riga[0], 12, 2) . "</td><td>" .
                                                      substr($riga[0], 14, 2) . "</td><td>" .
                                                      $riga[1] . "</td></tr>";
                mysqli_free_result($contrStatus);
            }
            // chiudi connessione db
            mysqli_close($connDB);
            fclose($file);
            echo "</tbody></table><br>";
            echo "FF = ON, 00 = OFF";
        } else { echo "NO CONTROLLERS CONFIGURED"; }
    ?>

</fieldset>

<br/>

<div id="login">
    <form action="subphp_/script.php" method="post">
        <b>Add Controller: </b>
        <input id="contr-add" name="contr-add" placeholder="Type Controller ID (Es: R00123)" type="text">
        <input name="submit" type="submit" value=" Add ">
    </form>
</div>

<div id="login">
    <form action="subphp_/script.php" method="post">
        <b>Remove Controller: </b>
        <input id="contr-del" name="contr-del" placeholder="Type Controller ID (Es: R00123)" type="text">
        <input name="submit" type="submit" value="Remove">
    </form>
</div>

<br/>
<br/>
<br/>

<h3 align="left" style="color:blue">MTTQ CHANNEL SETTINGS</h3>

<div id="login">
    <form action="subphp_/script.php" method="post">
        <b>Exchange host IP address: <br><i><?php $output=shell_exec("/var/www/html/script_/MANAGE_exchange"); print_r($output); ?></i></b>
        <input id="exch-ip" name="exch-ip" placeholder="Insert new IP address for the exchange" type="text">
        <input name="submit" type="submit" value="Change">
    </form>
</div>

<div id="login">
    <form action="subphp_/script.php" method="post">
        <b>Queue name: <br><i><?php $output=shell_exec("/var/www/html/script_/MANAGE_queue"); print_r($output); ?></i></b>
        <input id="queue_name" name="queue_name" placeholder="Insert new queue name" type="text">
        <input name="submit" type="submit" value="Change">
    </form>
</div>

</body>
</html>
