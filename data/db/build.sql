CREATE TABLE IF NOT EXISTS Users(
    username text PRIMARY KEY,
    server text
);

CREATE TABLE IF NOT EXISTS BookDragons(
    species text PRIMARY KEY,
    eggLine text DEFAULT "?",
    location text DEFAULT "?",
    price int DEFAULT -1,
    rarity text DEFAULT "?"
);

CREATE TABLE IF NOT EXISTS dragonBaseStats(
    species text,
    personality text,
    agility int DEFAULT -1,
    strength int DEFAULT -1,
    focus int DEFAULT -1,
    intellect int DEFAULT -1,
    FOREIGN KEY (species) REFERENCES BookDragons(species),
    FOREIGN KEY (personality) REFERENCES Personalities(personality)
);

CREATE TABLE IF NOT EXISTS OwnedDragons(
    dragon_id text PRIMARY KEY,
    username text,
    nickname text,
    species text,
    gender text,
    growth text,
    form text,
    viewCount text,
    personality text,
    FOREIGN KEY (species) REFERENCES BookDragons(species),
    FOREIGN KEY (username) REFERENCES Users(username),
    FOREIGN KEY (personality) REFERENCES Personalities(personality)
);

CREATE TABLE IF NOT EXISTS growingDragons(
    dragon_id text PRIMARY KEY,
    trainFor text,
    forTrade boolean,
    FOREIGN KEY (trainFor) REFERENCES Personalities(personality)
);

CREATE TABLE IF NOT EXISTS Personalities(
    personality text PRIMARY KEY,
    tier text,
    guaranteed boolean DEFAULT false,
    requirements text
);