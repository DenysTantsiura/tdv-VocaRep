<?php


$lang = 'en';
$text = 'hello world';

$curl = curl_init();
curl_setopt_array($curl, array(
    CURLOPT_URL => 'https://translate.google.com/_/TranslateWebserverUi/data/batchexecute',
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_CUSTOMREQUEST => 'POST',
    CURLOPT_POSTFIELDS => 'f.req=' . urlencode(json_encode([[['jQ1olc', '["' . $text . '","' . $lang . '",true,"null"]', '', 'generic']]]))
));
$response = curl_exec($curl);
curl_close($curl);
preg_match('#"(\/\/NE.*)"]"#', $response, $matches);
file_put_contents('/root/test.mp3', base64_decode($matches[1]));