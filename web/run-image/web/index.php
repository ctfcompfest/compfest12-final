<?php
    function create_image_id() {
        return sha1($_SERVER['REMOTE_ADDR'] . $_SERVER['HTTP_USER_AGENT'] . time() . mt_rand());
    }

    function remove_text_chunk($im){
        $pos = 8;
        $len = strlen($im);

        $ret = substr($im, 0, 8);
        while($pos < $len){
            $chunk_len = hexdec(bin2hex(substr($im, $pos, 4)));
            $chunk_type = substr($im, $pos + 4, 4);
            $chunk_all = substr($im, $pos, $chunk_len + 12);
            
            if ($chunk_type !== "tEXt" && $chunk_type !== "iTXt" && $chunk_type !== "zTXt" && $chunk_type !== "tIME") {
                $ret .= $chunk_all;
            }
            $pos += $chunk_len + 12;
        }

        return $ret;
    }

    if(isset($_POST['submit']) && isset($_FILES['image'])) {
        $fn = $_FILES['image']['tmp_name'];
    
        if(!is_uploaded_file($fn)) {
            die('uploaded file corrupted');
        }
    
        $iminfo = getimagesize($fn);
        if(!$iminfo) {
            die('input was not an image');
        }
        if($iminfo[0] > 32 || $iminfo[1] > 32) {
            die('image too big');
        }
        if(exif_imagetype($fn) !== IMAGETYPE_PNG) {
            die('only accept png file');
        }

        $contents = file_get_contents($fn);
        $save_contents = substr($contents, 0, strpos($contents, "IEND") + 8);  
        $save_contents = remove_text_chunk($save_contents);
        
        $im = imagecreatefromstring($save_contents);
        $im2 = imagecreatefrompng($fn);
        if(!$im || !$im2) {
            die('could not load your image');
        }
        imagedestroy($im); imagedestroy($im2);
            
        $imageid = create_image_id();
        $stt = file_put_contents("uploads/{$imageid}.png", $save_contents);
        if(!$stt){
            die("failed to save image");
        }

        header("Location: /run.php?id=$imageid");
    } else {
?>

<!DOCTYPE html>
<html>
    <head>
        <title>RunImage</title>
    </head>
    <body>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="image">Image file (max 32x32): </label>
            <input type="file" id="image" name="image" />
            <br />
            <input type="submit" name="submit" value="Run!" />
        </form>
    </body>
</html>
<?php
    }
?>