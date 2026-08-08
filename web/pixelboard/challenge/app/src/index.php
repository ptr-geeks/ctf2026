<?php
require_once __DIR__ . '/auth.php';

$user = current_user();
$db    = get_db();
$posts = $db->query(
    'SELECT posts.*, users.username, users.avatar
     FROM posts JOIN users ON users.id = posts.user_id
     ORDER BY posts.id DESC'
)->fetchAll(PDO::FETCH_ASSOC);

include __DIR__ . '/includes/header.php';
?>
<div class="bar">
<?php if ($user): ?>
  Prijavljen kot <b><?= h($user['username']) ?></b>
  · <a href="new_post.php">Nova objava</a>
  · <a href="profile.php">Moj profil</a>
  · <a href="logout.php">Odjava</a>
<?php else: ?>
  <a href="login.php">Prijava</a> za objavljanje in komentiranje.
<?php endif; ?>
</div>

<?php if (!$posts): ?>
  <p>Še ni objav.</p>
<?php endif; ?>

<?php foreach ($posts as $p): ?>
  <div class="card">
    <h3>
      <img class="avatar" src="uploads/<?= h($p['avatar']) ?>" alt="">
      <a href="post.php?id=<?= (int)$p['id'] ?>"><?= h($p['title']) ?></a>
    </h3>
    <?php if (!empty($p['image'])): ?>
      <img class="post-image" src="uploads/<?= h($p['image']) ?>" alt="">
    <?php endif; ?>
    <p style="white-space:pre-wrap"><?= h(mb_substr($p['body'], 0, 300)) ?></p>
    <div class="dim">— <?= h($p['username']) ?> · <?= h($p['created_at']) ?></div>
  </div>
<?php endforeach; ?>

<?php include __DIR__ . '/includes/footer.php'; ?>
