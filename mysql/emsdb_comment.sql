-- 删除表以防止表已存在而导致的错误（仅在需要时使用）
DROP TABLE IF EXISTS `Comment`;

CREATE TABLE `Comment` (
    ID INT AUTO_INCREMENT PRIMARY KEY,          -- CommentID
    UserID INT NOT NULL,                        -- ForeignKey to User.UserID
    Username VARCHAR(50) NOT NULL,
    Answer TEXT NOT NULL,
    AnsTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    EventID INT NOT NULL,                       -- ForeignKey to event.eventID
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (EventID) REFERENCES event(eventID)
);

-- 创建用户与评论的关系
-- ALTER TABLE Comment ADD CONSTRAINT fk_UserID FOREIGN KEY (UserID) REFERENCES User(UserID);
-- 创建事件与评论的关系
-- ALTER TABLE Comment ADD CONSTRAINT fk_EventID FOREIGN KEY (EventID) REFERE