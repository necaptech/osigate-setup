<?php
include('../session.php');

  if (isset($_POST['mysql-start']))   
   {
     shell_exec("/var/www/html/script_/MANAGE_mysql start");
     header("location: ../manage.php");
   } 
  elseif ( isset($_POST['mysql-stop']) )   
   {
     shell_exec("/var/www/html/script_/MANAGE_mysql stop");
     header("location: ../manage.php");
   } 
  elseif ( isset($_POST['httpd-reload']) )
   {
     shell_exec("/var/www/html/script_/MANAGE_httpd reload");
     header("location: ../manage.php");
   }
  elseif ( isset($_POST['evogw-stop']) )
   {
     shell_exec("/var/www/html/script_/MANAGE_evogw stop");
     header("location: ../manage.php");
   }
  elseif ( isset($_POST['upload-stop']) )
   {
     shell_exec("/var/www/html/script_/MANAGE_evogw upstop");
     header("location: ../manage.php");
   }
  elseif ( isset($_POST['sys-reboot']) )
   {
     shell_exec("/var/www/html/script_/MANAGE_reboot reboot");
     header("location: ../manage.php");
   }

  /* configure.php */
  elseif ( isset($_POST['sys-name']) )
   {
     $new_name=$_POST['sys-name'];
     shell_exec("/var/www/html/script_/MANAGE_system change '$new_name'");
     header("location: ../configure.php");
   }
  elseif ( isset($_POST['sys-proc']) )
   {
     $new_proc=$_POST['sys-proc'];
     shell_exec("/var/www/html/script_/MANAGE_process change '$new_proc'");
     header("location: ../configure.php");
   }
  elseif ( isset($_POST['apn-name']) )
   {
     $new_apn=$_POST['apn-name'];
     shell_exec("/var/www/html/script_/MANAGE_apn change '$new_apn'");
     header("location: ../configure.php");
   }
  elseif ( isset($_POST['usb-device']) )
   {
     $value=$_POST['usb-device'];
     shell_exec("/var/www/html/script_/MANAGE_usb change '$value'");
     header("location: ../configure.php");
   }
  elseif ( isset($_POST['sys-ssid']) ) /* && isset($_POST['sys-psk']) ) */
   {
     $new_ssid=$_POST['sys-ssid'];
     $new_psk=$_POST['sys-psk'];
     shell_exec("/var/www/html/script_/MANAGE_wifi setWIFI '$new_ssid' '$new_psk'");
     header("location: ../configure.php");
   }
  elseif ( isset($_POST['web-host']) )
   {
     $new_host=$_POST['web-host'];
     shell_exec("/var/www/html/script_/MANAGE_webhost change '$new_host'");
     header("location: ../configure.php");
   }
/* VT - marzo 2017: modifica per la configurazione da pannello del numero porta del web-server */
  elseif ( isset($_POST['web-host-port']) )
   {
     $new_hostPort=$_POST['web-host-port'];
     shell_exec("/var/www/html/script_/MANAGE_webhostPort change '$new_hostPort'");
     header("location: ../configure.php");
   }
/* VT - gennaio 2018: modifica per la configurazione da pannello del web-server aggiuntivo */
  elseif ( isset($_POST['additweb-host']) )
   {
     $new_addithost=$_POST['additweb-host'];
     shell_exec("/var/www/html/script_/MANAGE_additwebhost change '$new_addithost'");
     header("location: ../configure.php");
   }
  elseif ( isset($_POST['additweb-host-port']) )
   {
     $new_addithostPort=$_POST['additweb-host-port'];
     shell_exec("/var/www/html/script_/MANAGE_additwebhostPort change '$new_addithostPort'");
     header("location: ../configure.php");
   }


/* VT - utilizzo del dispositivo */
  elseif ( isset($_POST['application']) )
   {
     $new_applic=$_POST['application'];
     shell_exec("/var/www/html/script_/MANAGE_application set '$new_applic'");
     header("location: ../configure.php");
   }

  /* clients.php */
  elseif ( isset($_POST['blis-manage']) )
   {
     $command=$_POST['blis-manage'];
     $result=shell_exec("/var/www/html/script_/CLIENTS_manage '$command'");
     if ( $command == 3 )
       header("location: ../clients.php");
     else
       print_r($result);
   }
  elseif ( isset($_POST['blis-add']) )
   {
     $value=$_POST['blis-add'];
     shell_exec("/var/www/html/script_/CLIENTS_manage add '$value'");
     header("location: ../clients.php");
   }
  elseif ( isset($_POST['blis-del']) )
   {
     $value=$_POST['blis-del'];
     shell_exec("/var/www/html/script_/CLIENTS_manage del '$value'");
     header("location: ../clients.php");
   }

/* VT - gennaio 2019: timeOUT sui sensori per C2: Command & Control */
  elseif ( isset($_POST['tSTALE']) )
   {
     $new_tSTALE=$_POST['tSTALE'];
     shell_exec("/var/www/html/script_/MANAGE_tSTALE change '$new_tSTALE'");
     header("location: ../sensorc2.php");
   }
  elseif ( isset($_POST['tCONST']) )
   {
     $new_tCONST=$_POST['tCONST'];
     shell_exec("/var/www/html/script_/MANAGE_tCONST change '$new_tCONST'");
     header("location: ../sensorc2.php");
   }


/* controllers.php */
  elseif ( isset($_POST['contr-add']) )
   {
     $value=$_POST['contr-add'];
     shell_exec("/var/www/html/script_/CONTROLLERS_manage add '$value'");
     header("location: ../controllers.php");
   }
  elseif ( isset($_POST['contr-del']) )
   {
     $value=$_POST['contr-del'];
     shell_exec("/var/www/html/script_/CONTROLLERS_manage del '$value'");
     header("location: ../controllers.php");
   }
  elseif ( isset($_POST['tron1']) && isset($_POST['troff1']) )
   {
     $value1=$_POST['tron1'];
     $value2=$_POST['troff1'];
     shell_exec("/var/www/html/script_/MANAGE_tr set 1 '$value1' '$value2'");
     header("location: ../controllers.php");
   }

  elseif ( isset($_POST['tron2']) && isset($_POST['troff2']) )
   {
     $value1=$_POST['tron2'];
     $value2=$_POST['troff2'];
     shell_exec("/var/www/html/script_/MANAGE_tr set 2 '$value1' '$value2'");
     header("location: ../controllers.php");
   }

  elseif ( isset($_POST['tron3']) && isset($_POST['troff3']) )
   {
     $value1=$_POST['tron3'];
     $value2=$_POST['troff3'];
     shell_exec("/var/www/html/script_/MANAGE_tr set 3 '$value1' '$value2'");
     header("location: ../controllers.php");
   }

  elseif ( isset($_POST['tron4']) && isset($_POST['troff4']) )
   {
     $value1=$_POST['tron4'];
     $value2=$_POST['troff4'];
     shell_exec("/var/www/html/script_/MANAGE_tr set 4 '$value1' '$value2'");
     header("location: ../controllers.php");
   }

  elseif ( isset($_POST['tron5']) && isset($_POST['troff5']) )
   {
     $value1=$_POST['tron5'];
     $value2=$_POST['troff5'];
     shell_exec("/var/www/html/script_/MANAGE_tr set 5 '$value1' '$value2'");
     header("location: ../controllers.php");
   }

  elseif ( isset($_POST['tron6']) && isset($_POST['troff6']) )
   {
     $value1=$_POST['tron6'];
     $value2=$_POST['troff6'];
     shell_exec("/var/www/html/script_/MANAGE_tr set 6 '$value1' '$value2'");
     header("location: ../controllers.php");
   }

  elseif ( isset($_POST['tron7']) && isset($_POST['troff7']) )
   {
     $value1=$_POST['tron7'];
     $value2=$_POST['troff7'];
     shell_exec("/var/www/html/script_/MANAGE_tr set 7 '$value1' '$value2'");
     header("location: ../controllers.php");
   }

  elseif ( isset($_POST['tron8']) && isset($_POST['troff8']) )
   {
     $value1=$_POST['tron8'];
     $value2=$_POST['troff8'];
     shell_exec("/var/www/html/script_/MANAGE_tr set 8 '$value1' '$value2'");
     header("location: ../controllers.php");
   }





/* exchange settings */
  elseif ( isset($_POST['exch-ip']) )
   {
     $new_ip=$_POST['exch-ip'];
     shell_exec("/var/www/html/script_/MANAGE_exchange change '$new_ip'");
     header("location: ../controllers.php");
   }
  elseif ( isset($_POST['queue_name']) )
   {
     $new_q=$_POST['queue_name'];
     shell_exec("/var/www/html/script_/MANAGE_queue change '$new_q'");
     header("location: ../controllers.php");
   }


  /* statistics.php */
  elseif (isset($_POST['mysql-query']))
   {
     $new_query=$_POST['mysql-query'];

     $list_opt=$_POST['cli'];

     if ( $new_query == "11a" )
       {
       $cid=$_POST['cli1'];
       $qty=$_POST['qty1'];
       $fromyear=$_POST['fromyear1'];
       $frommonth=$_POST['frommonth1'];
       $fromday=$_POST['fromday1'];
       $fromhour=$_POST['fromhour1'];
       $fromminute=$_POST['fromminute1'];
       $toyear=$_POST['toyear1'];
       $tomonth=$_POST['tomonth1'];
       $today=$_POST['today1'];
       $tohour=$_POST['tohour1'];
       $tominute=$_POST['tominute1'];
       foreach ($_POST as $key => $value) 
         {
         shell_exec("echo '$key'-'$value' >> /tmp/script.php.log");
         }
       }
     elseif ( $new_query == "14a" )
       {
       $cid=$_POST['cli2'];
       $qty=$_POST['qty2'];
       $fromyear=$_POST['fromyear2'];
       $frommonth=$_POST['frommonth2'];
       $fromday=$_POST['fromday2'];
       $fromhour=$_POST['fromhour2'];
       $fromminute=$_POST['fromminute2'];
       $toyear=$_POST['toyear2'];
       $tomonth=$_POST['tomonth2'];
       $today=$_POST['today2'];
       $tohour=$_POST['tohour2'];
       $tominute=$_POST['tominute2'];
       foreach ($_POST as $key => $value)
         {
         shell_exec("echo '$key'-'$value' >> /tmp/script.php.log");
         }
       }
     elseif ( $new_query == "3a" )
       {
       $cid=$_POST['cli11'];
       $qty=$_POST['qty11'];
       $getres=shell_exec("/var/www/html/script_/STATISTIC_mysql query '$new_query' '$cid' '$qty'");
       }
     elseif ( $new_query == "15a" )
       {
       $cid=$_POST['cli3'];
       $qty=$_POST['qty3'];
       $fromyear=$_POST['fromyear3'];
       $frommonth=$_POST['frommonth3'];
       $fromday=$_POST['fromday3'];
       $fromhour=$_POST['fromhour3'];
       $fromminute=$_POST['fromminute3'];
       $toyear=$_POST['toyear3'];
       $tomonth=$_POST['tomonth3'];
       $today=$_POST['today3'];
       $tohour=$_POST['tohour3'];
       $tominute=$_POST['tominute3'];
       foreach ($_POST as $key => $value)
         {
         shell_exec("echo '$key'-'$value' >> /tmp/script.php.log");
         }
       }
     
     if ( !empty($qty) )
       {
       $getres=shell_exec("/var/www/html/script_/STATISTIC_mysql query '$new_query' '$cid' '$qty' '$fromyear' '$frommonth' '$fromday' '$fromhour' '$fromminute' '$toyear' '$tomonth' '$today' '$tohour' '$tominute'");
       }
     else
       $getres=shell_exec("/var/www/html/script_/STATISTIC_mysql query '$new_query' '$list_opt'");

     print_r($getres);
   }
  elseif (isset($_POST['mysql-dump']))
   {
     $new_query=$_POST['mysql-dump'];
     $getres=shell_exec("/var/www/html/script_/STATISTIC_mysql dump '$new_query'");
     print_r($getres);
   }
  elseif (isset($_POST['csv-export']))
   {
     $new_query=$_POST['csv-export'];
     $getres=shell_exec("/var/www/html/script_/STATISTIC_mysql export '$new_query'");
     print_r($getres);
   }

  // if no option isset
  elseif ( isset($_POST['submit']) )
   {
     $value=$_POST['submit'];
     if ( $value == 'Reset' )
      {
       shell_exec("/var/www/html/script_/CLIENTS_manage '$value'");
       header("location: ../clients.php");
      }
     elseif ( $value == 'Query' )
      {
       header("location: ../statistics.php");
      }

     else
      echo "CIAOOOO";
   }
?>
