create database esd;
use esd;
CREATE TABLE IF NOT EXISTS `account` (
  `fullname` varchar(64),
  `passwd` varchar(64),
  `email` varchar(64) NOT NULL,
  PRIMARY KEY (email)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE follower (
  email varchar(64) NOT NULL,
  followemail varchar(64) NOT NULL,
  PRIMARY KEY (email, followemail),
  FOREIGN KEY (email) references account(email),
  FOREIGN KEY (followemail) references account(email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE listing( 
	listing_id INT NOT NULL AUTO_INCREMENT, 
    quantity DECIMAL(10,2) NOT NULL,
    currqty  DECIMAL(10,2),
    postTime TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    startTime DATETIME NOT NULL, 
    endTime DATETIME NOT NULL, 
    productName VARCHAR(64) NOT NULL, 
    description VARCHAR(256) NOT NULL, 
    price DECIMAL(10, 2) NOT NULL, 
    category VARCHAR(16) NOT NULL, 
    availability BOOLEAN NOT NULL, 
    location VARCHAR(64) NOT NULL, 
    unit VARCHAR(16) NOT NULL, 
    phoneNumber CHAR(8) NOT NULL,
    sellername VARCHAR(64),
    selleremail VARCHAR(64),
    image VARCHAR(256),
    PRIMARY KEY(listing_id)
) ENGINE = InnoDB;

CREATE TABLE orders( 
	order_id INT AUTO_INCREMENT,
	listing_id INT NOT NULL, 
    buyqty DECIMAL(10,2) NOT NULL,
    buyerphone INT, 
    price DECIMAL(10, 2) NOT NULL,
    buyeremail VARCHAR(64),
    selleremail VARCHAR(64),
    paymenttoken VARCHAR(128),
    googlepay BOOLEAN,
    PRIMARY KEY(order_id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `error` (
  `error_id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(32) NOT NULL,
  PRIMARY KEY (`error_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `activity_log`;
CREATE TABLE IF NOT EXISTS `activity_log` (
  `activity_log_id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(32) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`activity_log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

INSERT INTO listing(quantity, currqty, postTime, startTime, endTime, productName, description, price, category, availability, location, unit, phoneNumber, sellername, selleremail, image ) VALUES( '10', "5", " ", '2022-03-31 17:06:15', '2022-04-02 17:06:15', 'Durians', 'Delicious Durians, looking for 5 more buyers! SHARE SHARE W me now!!', '22.2', 'Food Delivery', 1, 'Tampines', 'piece', '91234567', 'Min', 'heyitsminai@gmail.com', 'https://images.unsplash.com/photo-1562486683-67d4d5886f99?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=775&q=80' );

INSERT INTO listing(quantity, currqty, postTime, startTime, endTime, productName, description, price, category, availability, location, unit, phoneNumber, sellername, selleremail, image ) VALUES('100', "50", " ", '2022-04-01 18:06:15', '2022-04-08 12:00:00', 'Bulk buying of stationaries', 'Looking to buy stationaries! Join me now please!!', '5', 'E-commerce', 1, 'Singapore Management University', 'piece', '91234567', 'Min', 'heyitsminai@gmail.com', 'https://images.unsplash.com/photo-1528938102132-4a9276b8e320?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80' );

INSERT INTO listing(quantity, currqty, postTime, startTime, endTime, productName, description, price, category, availability, location, unit, phoneNumber, sellername, selleremail, image ) VALUES("80", "16.5", " ", '2022-04-04 12:00:00', '2022-04-08 12:00:00', 'Grocery Sharing', 'Hi, Looking to hit $100 for free delivery! Please join me!', '','Daily Needs', 1, 'Singapore Management University', '', '99934567', 'bella', 'bluseabella@gmail.com', 'https://images.unsplash.com/photo-1588964895597-cfccd6e2dbf9?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1074&q=80');

INSERT INTO listing(quantity, currqty, postTime, startTime, endTime, productName, description, price, category, availability, location, unit, phoneNumber, sellername, selleremail, image ) VALUES('1', "0", " ", '2022-03-31 17:00:15', '2022-04-10 17:06:15', 'Share Starbucks 1-1 with me. I no friend,sad life..', 'I wanted to buy starbucks Choc Chip Frappe Venti 1-1 at 1pm on 27th Dec!Join me now! We split cost!Fast Finger first!', '4.55', 'Daily Needs', 1, 'Tampines', 'bottle', '91234560', 'YM', 'yimei@gmail.com', 'https://cdn.greatdeals.com.sg/wp-content/uploads/2020/11/22130157/starbucks-sg-1-for-1-treat-nov-2020.jpg.webp' );

INSERT INTO listing(quantity, currqty, postTime, startTime, endTime, productName, description, price, category, availability, location, unit, phoneNumber, sellername, selleremail, image ) VALUES('90', "10", " ", '2022-03-31 17:00:15', '2022-04-10 17:06:15', 'Shopee Innisfree shop fulfill $90 together for free delivery from Korea', 'Choose any product from here.https://shopee.sg/rossy.sg?categoryId=100&itemId=2624 To reach $90 store-wide for free delivery. Once paid,I will place order for you & notify you when parcels arrive.', '', 'E-commerce', 1, 'Tampines', '', '91234560', 'YM', 'yimei@gmail.com', 'https://cf.shopee.sg/file/be628924b403c63333d34a77c9d3ee9e' );

INSERT INTO listing(quantity, currqty, postTime, startTime, endTime, productName, description, price, category, availability, location, unit, phoneNumber, sellername, selleremail, image ) VALUES('80', "10", " ", '2022-04-09 17:00:15', '2022-04-10 17:06:15', 'Grab Seoul Garden@Clementi to reach $80 min order to eliminate small order fee + free delivery', 'Small order fee=$10,delivery fee=$9.5. Choose any food on Grab in this restaurant ,Seoul Garden@Clementi. Submit order to me by 1pm 26 Dec 2022 to reach $80 min order for free delivery! Will notify for pickup at blk 432 Eunos S230432 once food arrived.', '', 'Food delivery', 1, 'Clementi', '', '91234560', 'YM', 'yimei@gmail.com', 'https://www.grab.com/sg/wp-content/uploads/sites/4/2018/06/GrabFood-logo-1.jpg' );

INSERT INTO listing(quantity, currqty, postTime, startTime, endTime, productName, description, price, category, availability, location, unit, phoneNumber, sellername, selleremail, image ) VALUES('10', "0", " ", '2022-03-31 17:00:15', '2022-04-10 17:06:15', '10 boxes of haagen dazs chocolate ice cream to share! ', 'I have 10 boxes of haagen dazs chocolate ice cream that I cannot finish. Expiry date 1 March 2023.', '', 'Daily Needs', 1, 'Clementi', '', '91234560', 'YM', 'yimei@gmail.com', 'https://media.nedigital.sg/fairprice/fpol/media/images/product/XL/11576937_XL1_20210118.jpg' );

INSERT INTO ACCOUNT VALUES ("YM", "superstronk", "yimei@gmail.com");

INSERT INTO ACCOUNT VALUES ("bella", "stronkpassword", "bluseabella@gmail.com");

INSERT INTO ACCOUNT VALUES ("min", "morestronkpassword", "heyitsminai@gmail.com");

select * from listing;