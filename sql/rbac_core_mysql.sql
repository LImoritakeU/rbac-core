CREATE TABLE `object` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT
);

CREATE TABLE `operation` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT
);

CREATE TABLE `permission` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) UNIQUE NOT NULL,
  `create_at` DATETIME NOT NULL,
  `update_at` DATETIME NOT NULL
);

CREATE TABLE `object_permissions` (
  `permission` INTEGER NOT NULL,
  `object` INTEGER NOT NULL,
  CONSTRAINT `pk_object_permissions` PRIMARY KEY (`permission`, `object`)
);

CREATE INDEX `idx_object_permissions` ON `object_permissions` (`object`);

ALTER TABLE `object_permissions` ADD CONSTRAINT `fk_object_permissions__object` FOREIGN KEY (`object`) REFERENCES `object` (`id`);

ALTER TABLE `object_permissions` ADD CONSTRAINT `fk_object_permissions__permission` FOREIGN KEY (`permission`) REFERENCES `permission` (`id`);

CREATE TABLE `operation_permissions` (
  `permission` INTEGER NOT NULL,
  `operation` INTEGER NOT NULL,
  CONSTRAINT `pk_operation_permissions` PRIMARY KEY (`permission`, `operation`)
);

CREATE INDEX `idx_operation_permissions` ON `operation_permissions` (`operation`);

ALTER TABLE `operation_permissions` ADD CONSTRAINT `fk_operation_permissions__operation` FOREIGN KEY (`operation`) REFERENCES `operation` (`id`);

ALTER TABLE `operation_permissions` ADD CONSTRAINT `fk_operation_permissions__permission` FOREIGN KEY (`permission`) REFERENCES `permission` (`id`);

CREATE TABLE `role` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) UNIQUE NOT NULL,
  `create_at` DATETIME NOT NULL,
  `update_at` DATETIME NOT NULL
);

CREATE TABLE `permission_roles` (
  `role` INTEGER NOT NULL,
  `permission` INTEGER NOT NULL,
  CONSTRAINT `pk_permission_roles` PRIMARY KEY (`role`, `permission`)
);

CREATE INDEX `idx_permission_roles` ON `permission_roles` (`permission`);

ALTER TABLE `permission_roles` ADD CONSTRAINT `fk_permission_roles__permission` FOREIGN KEY (`permission`) REFERENCES `permission` (`id`);

ALTER TABLE `permission_roles` ADD CONSTRAINT `fk_permission_roles__role` FOREIGN KEY (`role`) REFERENCES `role` (`id`);

CREATE TABLE `user` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `create_at` DATETIME NOT NULL,
  `update_at` DATETIME NOT NULL
);

CREATE TABLE `role_users` (
  `user` INTEGER NOT NULL,
  `role` INTEGER NOT NULL,
  CONSTRAINT `pk_role_users` PRIMARY KEY (`user`, `role`)
);

CREATE INDEX `idx_role_users` ON `role_users` (`role`);

ALTER TABLE `role_users` ADD CONSTRAINT `fk_role_users__role` FOREIGN KEY (`role`) REFERENCES `role` (`id`);

ALTER TABLE `role_users` ADD CONSTRAINT `fk_role_users__user` FOREIGN KEY (`user`) REFERENCES `user` (`id`);

CREATE TABLE `session` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `create_at` DATETIME,
  `user` INTEGER NOT NULL
);

CREATE INDEX `idx_session__user` ON `session` (`user`);

ALTER TABLE `session` ADD CONSTRAINT `fk_session__user` FOREIGN KEY (`user`) REFERENCES `user` (`id`);

CREATE TABLE `role_sessions` (
  `role` INTEGER NOT NULL,
  `session` INTEGER NOT NULL,
  CONSTRAINT `pk_role_sessions` PRIMARY KEY (`role`, `session`)
);

CREATE INDEX `idx_role_sessions` ON `role_sessions` (`session`);

ALTER TABLE `role_sessions` ADD CONSTRAINT `fk_role_sessions__role` FOREIGN KEY (`role`) REFERENCES `role` (`id`);

ALTER TABLE `role_sessions` ADD CONSTRAINT `fk_role_sessions__session` FOREIGN KEY (`session`) REFERENCES `session` (`id`)