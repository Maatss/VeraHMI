<?
ini_set('set_time_limit', 50);

$data = shell_exec('sudo /usr/bin/python write.py 1 '.$_GET['id'].' 1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+16+17+18+19+20+21+22+23+24+25+26+27+28+29+30+31+32+33+34+35+36+37+38+39+40+41+42');
//$data = shell_exec('whoami');


$data = str_replace(" ", "=",$data);

if(strpos($data, "#OK:") === 0){
	$p = explode(":", $data);
	$p = explode("&", $p[1]);
		
	$p =  explode("+",$p[0]);
	
	$arr = array();
	$i = 1;
	foreach($p as $d){
		$arr["d".$i] = $d;
		$i++;
	}
	echo json_encode($arr);
} else {
	echo "No data (or trash): \n";
    //echo $data
}
?>