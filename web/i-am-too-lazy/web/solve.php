<?php

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    echo "Forbidden";
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['mathex'])) {
        $var = $_POST['mathex'];

        $out = serialize(array("solvemathex", $var));
        $encoded = base64_encode($out);
        if ($_SERVER["SERVER_PORT"] != "80") {
            header("Location: http://".$_SERVER["SERVER_NAME"].":".$_SERVER["SERVER_PORT"]."/?input=".$encoded, true, 302); 
        } else {
            header("Location: http://".$_SERVER["SERVER_NAME"]."/?input=".$encoded, true, 302); 
        }
        exit();
    } else {
        if ($_SERVER["SERVER_PORT"] != "80") {
            header("Location: http://".$_SERVER["SERVER_NAME"].":".$_SERVER["SERVER_PORT"], true, 302); 
        } else {
            header("Location: http://".$_SERVER["SERVER_NAME"], true, 302); 
        }
        exit();
    }
}
?>