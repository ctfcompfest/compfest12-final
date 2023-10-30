<?php
if(isset($_GET['id'])) {
    if(1 !== preg_match('/[0-9a-f]{40}/', $_GET['id'])) {
        die('invalid file id');
    }

    include("uploads/".$_GET['id'].".png");
} else {
    header("Location: /");
}
?>