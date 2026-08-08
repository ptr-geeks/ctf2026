<?php
require_once __DIR__ . '/auth.php';

$user    = require_login();
$error   = '';
$success = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['avatar'])) {
    $file = $_FILES['avatar'];

    if ($file['error'] !== UPLOAD_ERR_OK) {
        $error = 'Nalaganje datoteke ni uspelo.';
    } else {
        $header = file_get_contents($file['tmp_name'], false, null, 0, 8);
        $signatures = [
            "\xFF\xD8\xFF",       // JPEG
            "\x89PNG\r\n\x1a\n",  // PNG
            "GIF87a",             // GIF
            "GIF89a",             // GIF
        ];

        $valid = false;
        foreach ($signatures as $magic) {
            if (substr($header, 0, strlen($magic)) === $magic) {
                $valid = true;
                break;
            }
        }

        if (!$valid) {
            $error = 'Datoteka ni veljavna slika (napačna glava datoteke).';
        } else {
            $filename = basename($file['name']);
            $dest     = __DIR__ . '/uploads/' . $filename;
            move_uploaded_file($file['tmp_name'], $dest);

            $db   = get_db();
            $stmt = $db->prepare('UPDATE users SET avatar = :avatar WHERE id = :id');
            $stmt->execute([':avatar' => $filename, ':id' => $user['id']]);

            $user['avatar'] = $filename;
            $success        = 'Profilna slika je bila posodobljena.';
        }
    }
}

include __DIR__ . '/includes/header.php';
?>
<p><a href="index.php">← Nazaj na desko</a></p>
<h1>Profil — <?= h($user['username']) ?></h1>
<?php if ($error): ?><p class="error"><?= h($error) ?></p><?php endif; ?>
<?php if ($success): ?><p class="success"><?= h($success) ?></p><?php endif; ?>
<p><img class="avatar" style="width:96px;height:96px" src="uploads/<?= h($user['avatar']) ?>" alt=""></p>
<form method="post" enctype="multipart/form-data">
  <label>Nova profilna slika (jpg, png ali gif)</label>
  <input type="file" name="avatar" required>
  <button type="submit">Naloži</button>
</form>
<?php include __DIR__ . '/includes/footer.php'; ?>
