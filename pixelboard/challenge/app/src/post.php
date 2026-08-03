<?php
require_once __DIR__ . '/auth.php';

$id   = (int)($_GET['id'] ?? 0);
$db   = get_db();
$user = current_user();

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $user) {
    $body = trim($_POST['body'] ?? '');
    if ($body !== '') {
        $stmt = $db->prepare(
            'INSERT INTO comments (post_id, user_id, body, created_at) VALUES (:pid, :uid, :body, :ts)'
        );
        $stmt->execute([
            ':pid'  => $id,
            ':uid'  => $user['id'],
            ':body' => $body,
            ':ts'   => date('c'),
        ]);
    }
}

$stmt = $db->prepare(
    'SELECT posts.*, users.username FROM posts JOIN users ON users.id = posts.user_id WHERE posts.id = :id'
);
$stmt->execute([':id' => $id]);
$post = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$post) {
    http_response_code(404);
    include __DIR__ . '/includes/header.php';
    echo '<p class="error">Objava ne obstaja.</p>';
    include __DIR__ . '/includes/footer.php';
    exit;
}

$stmt = $db->prepare(
    'SELECT comments.*, users.username FROM comments JOIN users ON users.id = comments.user_id
     WHERE post_id = :id ORDER BY comments.id ASC'
);
$stmt->execute([':id' => $id]);
$comments = $stmt->fetchAll(PDO::FETCH_ASSOC);

include __DIR__ . '/includes/header.php';
?>
<p><a href="index.php">← Nazaj na desko</a></p>
<h1><?= h($post['title']) ?></h1>
<p class="dim">— <?= h($post['username']) ?> · <?= h($post['created_at']) ?></p>
<?php if (!empty($post['image'])): ?>
  <img class="post-image" src="uploads/<?= h($post['image']) ?>" alt="">
<?php endif; ?>
<p style="white-space:pre-wrap"><?= h($post['body']) ?></p>
<hr>
<h2>Komentarji</h2>
<?php if (!$comments): ?><p class="dim">Ni komentarjev.</p><?php endif; ?>
<?php foreach ($comments as $c): ?>
  <div class="card"><b><?= h($c['username']) ?>:</b> <?= h($c['body']) ?></div>
<?php endforeach; ?>

<?php if ($user): ?>
<form method="post">
  <textarea name="body" placeholder="Napiši komentar..." required></textarea>
  <button type="submit">Komentiraj</button>
</form>
<?php else: ?>
<p><a href="login.php">Prijavi se</a>, da lahko komentiraš.</p>
<?php endif; ?>
<?php include __DIR__ . '/includes/footer.php'; ?>
