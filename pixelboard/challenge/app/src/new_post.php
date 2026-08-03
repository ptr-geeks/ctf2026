<?php
require_once __DIR__ . '/auth.php';

$user  = require_login();
$error = '';

const ALLOWED_IMAGE_TYPES = [
    IMAGETYPE_JPEG => 'jpg',
    IMAGETYPE_PNG  => 'png',
    IMAGETYPE_GIF  => 'gif',
    IMAGETYPE_WEBP => 'webp',
];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = trim($_POST['title'] ?? '');
    $body  = trim($_POST['body'] ?? '');
    $image = null;

    if ($title === '' || $body === '') {
        $error = 'Naslov in vsebina sta obvezna.';
    } elseif (!empty($_FILES['image']['name']) && $_FILES['image']['error'] !== UPLOAD_ERR_NO_FILE) {
        $file = $_FILES['image'];
        if ($file['error'] !== UPLOAD_ERR_OK) {
            $error = 'Nalaganje slike ni uspelo.';
        } else {
            $info = @getimagesize($file['tmp_name']);
            if ($info === false || !isset(ALLOWED_IMAGE_TYPES[$info[2]])) {
                $error = 'Priložena datoteka ni veljavna slika (jpg, png, gif ali webp).';
            } else {
                $ext      = ALLOWED_IMAGE_TYPES[$info[2]];
                $filename = bin2hex(random_bytes(16)) . '.' . $ext;
                move_uploaded_file($file['tmp_name'], __DIR__ . '/uploads/' . $filename);
                $image = $filename;
            }
        }
    }

    if ($error === '') {
        $db   = get_db();
        $stmt = $db->prepare(
            'INSERT INTO posts (user_id, title, body, image, created_at) VALUES (:uid, :title, :body, :image, :ts)'
        );
        $stmt->execute([
            ':uid'   => $user['id'],
            ':title' => $title,
            ':body'  => $body,
            ':image' => $image,
            ':ts'    => date('c'),
        ]);
        header('Location: index.php');
        exit;
    }
}

include __DIR__ . '/includes/header.php';
?>
<p><a href="index.php">← Nazaj na desko</a></p>
<h1>Nova objava</h1>
<?php if ($error): ?><p class="error"><?= h($error) ?></p><?php endif; ?>
<form method="post" enctype="multipart/form-data">
  <input type="text" name="title" placeholder="Naslov" required>
  <textarea name="body" placeholder="O čem razmišljate?" required></textarea>
  <label>Slika (neobvezno — jpg, png, gif ali webp)</label>
  <input type="file" name="image" accept="image/*">
  <button type="submit">Objavi</button>
</form>
<?php include __DIR__ . '/includes/footer.php'; ?>
