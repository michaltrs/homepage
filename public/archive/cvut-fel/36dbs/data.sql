INSERT INTO Pavilon(nazev,c_pav) VALUES ('äelmy',10);
INSERT INTO Pavilon(nazev,c_pav) VALUES ('MedvÏdi',20);
INSERT INTO Pavilon(nazev,c_pav) VALUES ('Opice',30 );
INSERT INTO Pavilon(nazev,c_pav) VALUES ('LichokopytnÌci a hlodavci',40);
INSERT INTO Pavilon(nazev,c_pav) VALUES ('Plaz',50);

INSERT INTO Vybeh(Pavi_c_pav,c_vyb,nazev,max_zvirat) VALUES (10,1,'KoËkovitÈ z Afriky',10);
INSERT INTO Vybeh(Pavi_c_pav,c_vyb,nazev,max_zvirat) VALUES (10,2,'KoËkovitÈ z Asie',7);
INSERT INTO Vybeh(Pavi_c_pav,c_vyb,nazev,max_zvirat) VALUES (10,3,'KoËkovitÈ z Ameriky',5);
INSERT INTO Vybeh(Pavi_c_pav,c_vyb,nazev,max_zvirat) VALUES (10,4,'DrobnÈ öelmy',6);
INSERT INTO Vybeh(Pavi_c_pav,c_vyb,nazev,max_zvirat) VALUES (20,1,'MedvÏdi',4);
INSERT INTO Vybeh(Pavi_c_pav,c_vyb,nazev,max_zvirat) VALUES (20,2,'MedvÌdci',4);
INSERT INTO Vybeh(Pavi_c_pav,c_vyb,nazev,max_zvirat) VALUES (10,5,'KunovitÈ',10);
INSERT INTO Vybeh(Pavi_c_pav,c_vyb,nazev,max_zvirat) VALUES (30,1,'malpovÈ a kosmanovÈ',5);
INSERT INTO Vybeh(Pavi_c_pav,c_vyb,nazev,max_zvirat) VALUES (30,2,'koËkodanovÈ',5);
INSERT INTO Vybeh(Pavi_c_pav,c_vyb,nazev,max_zvirat) VALUES (40,1,'LichokopytnÌci',15);
INSERT INTO Vybeh(Pavi_c_pav,c_vyb,nazev,max_zvirat) VALUES (40,2,'Hlodavci',20);
INSERT INTO Vybeh(Pavi_c_pav,c_vyb,nazev,max_zvirat) VALUES (50,1,'jeötÏ¯i',20);
INSERT INTO Vybeh(Pavi_c_pav,c_vyb,nazev,max_zvirat) VALUES (50,2,'Hadi',10);


INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Irbis','Fanouöek',to_date('2001-06-19','yyyy-mm-dd'),'st¯ednÌ Asie','horötÌ kopytnÌci a jinÌ menöÌ savci',1,10,2);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Karakal','Miö·',to_date('1983-06-22','yyyy-mm-dd'),'Afrika','zvÌ¯ata do velikosti gazel',1,10,1);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('KoËka baûinn·','Zuzanka',to_date('1984-07-19','yyyy-mm-dd'),'Asie','menöÌ savci, p¯ev·ûnÏ hlodavci',2,10,2);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('KoËka divok·','HonzÌk',to_date('2000-04-20','yyyy-mm-dd'),'Afrika','drobn· zvÌ¯ata, hlodavce',2,10,1);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Levhart cejlonsk˝','JaniËka',to_date('1995-06-03','yyyy-mm-dd'),'SrÌ Lanka','jeleny, antilopy, opice',1,10,2);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Levhart persk˝','Eliöka',to_date('1997-02-09','yyyy-mm-dd'),'jiûnÌ Asie','jeleny, antilopy, opice',1,10,2);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Margay','PepÌk',to_date('1980-08-17','yyyy-mm-dd'),'Amerika','zvÌ¯ata ûijÌcÌ na stromech, krysy,myöi',2,10,3);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Rys Ëerven˝','Monika',to_date('1980-12-02','yyyy-mm-dd'),'SevernÌ Amerika','menöÌ savci (zajÌci, hlodavci...)',2,10,3);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Serval','LadÌk',to_date('1986-11-09','yyyy-mm-dd'),'Afrika','drobn· zvÌ¯ata, pt·ky',2,10,1);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Tygr sumatersk˝','Tom',to_date('1979-10-14','yyyy-mm-dd'),'ostrov Sumatra','prasata, jeleny',1,10,2);


INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Kolonok','Petr',to_date('1980-02-25','yyyy-mm-dd'),'jihov˝chodnÌ Asie','hlodavci, obojûivelnÌci, ryby',2,10,4);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Kolonok','Karla',to_date('1981-12-21','yyyy-mm-dd'),'jihov˝chodnÌ Asie','hlodavci, obojûivelnÌci, ryby',2,10,4);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Mangusta ûÌhan·','Tereza',to_date('2000-05-13','yyyy-mm-dd'),'Afrika','p¯ev·ûnÏ ûivoËiön·',2,10,4);



INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('MedvÏd malajsk˝','BruËÌk',to_date('1989-09-16','yyyy-mm-dd'),'jihov˝chodnÌ Asie','vöeûravec',1,20,1);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('MedvÏd malajsk˝','PinÔa',to_date('1992-01-10','yyyy-mm-dd'),'jihov˝chodnÌ Asie','vöeûravec',1,20,1);

INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('M˝val severnÌ','Miö·k',to_date('1982-04-15','yyyy-mm-dd'),'SevernÌ Amerika','vöeûravec',2,20,2);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('M˝val severnÌ','ZuzÌk',to_date('1980-07-11','yyyy-mm-dd'),'SevernÌ Amerika','vöeûravec',2,20,2);


INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Skunk pruhovan˝','Romana',to_date('1987-07-08','yyyy-mm-dd'),'SevernÌ Amerika','ûivoËiön· i rostlinn·',2,10,5);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Tcho¯Ìk skvrnit˝','KajÌk',to_date('1986-04-15','yyyy-mm-dd'),'Balk·n','hraboöi,hmyz,piöùuchy',2,10,5);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Vydra mal·','BobÌk',to_date('2000-09-10','yyyy-mm-dd'),'jihov˝chodnÌ Asie','kor˝öe, mÏk˝öe, ryby',3,10,5);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Vydra mal·','AlÌk',to_date('2003-01-15','yyyy-mm-dd'),'jihov˝chodnÌ Asie','kor˝öe, mÏk˝öe, ryby',3,10,5);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Vydra mal·','KajÌk',to_date('1998-10-12','yyyy-mm-dd'),'jihov˝chodnÌ Asie','kor˝öe, mÏk˝öe, ryby',3,10,5);

INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Chvostan bÏlolÌcÌ','EviËka',to_date('1999-08-07','yyyy-mm-dd'),'JiûnÌ Amerika','rostlinn· i ûivoËiön·',3,30,1);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Kalimiko','Filip',to_date('1997-04-28','yyyy-mm-dd'),'JiûnÌ Amerika','hmyz, ptaËÌ vejce, semena, plody',4,30,1);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Kosman bÏloËel˝','P·ja',to_date('2000-08-15','yyyy-mm-dd'),'JiûnÌ Amerika','semena, plody, hmyz',2,30,1);

INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('KoËkodan Campbell˘v','Ruda',to_date('1980-05-19','yyyy-mm-dd'),'z·padnÌ Afrika','plody, listy, drobnÌ ûivoËichovÈ',3,30,2);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Makak tmav˝','Lucinka',to_date('2001-09-01','yyyy-mm-dd'),'ostrov Sulawesi','rostlinn·',4,30,2);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Mangabej Ëern˝','PavlÌk',to_date('2000-08-09','yyyy-mm-dd'),'rovnÌkov· Afrika','tvrd· semena, o¯echy',4,30,2);

INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('K˘Ú dom·cÌ','Alice',to_date('2000-08-25','yyyy-mm-dd'),'poch·zÌ ze Shetlandsk˝ch ostrov˘','rostlinn·',3,40,1);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('TapÌr jihoamerick˝','Luk·ö',to_date('1998-01-20','yyyy-mm-dd'),'JiûnÌ Amerika','rostlinn· potrava',3,40,1);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Zebra damarsk·','ToniËka',to_date('1991-03-09','yyyy-mm-dd'),'jihov˝chodnÌ Afrika','stepnÌ traviny',4,40,1);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Kapybara','Pet¯Ìk',to_date('1984-05-20','yyyy-mm-dd'),'JiûnÌ Amerika','traviny',5,40,2);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Psoun preriov˝','Verunka',to_date('2001-09-18','yyyy-mm-dd'),'SevernÌ Amerika','rostlinn·',5,40,2);

INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Korovec jedovat˝','PepÌno',to_date('2001-08-19','yyyy-mm-dd'),'St¯ednÌ Amerika','hlodavci, hmyz, pt·Ëata, vejce',2,50,1);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Krokod˝l Ëelnat˝','Tereza',to_date('1998-07-10','yyyy-mm-dd'),'z·padnÌ Afrika','malÌ obratlovci, kor˝öi',1,50,1);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Zmije obecn·','Rudolf',to_date('2002-08-17','yyyy-mm-dd'),'Evropa','drobnÌ savci, jeötÏrky',3,50,2);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Kobra ËÌnsk·','Emil',to_date('1998-04-01','yyyy-mm-dd'),'jihov˝chodnÌ Asie','hlodavci, hadi, jeötÏ¯i',2,50,2);
INSERT INTO Zvire(nazev,jmeno,dat_nar,puvod,potrava,frek_krmeni,vybeh__Pavi_c_pav,vybeh__c_vyb) 
	VALUES ('Krajta ostrovnÌ','Radka',to_date('2000-01-09','yyyy-mm-dd'),'IndonÈsie','hlodavci',2,50,2);

 
INSERT INTO Zamestnanec(Jmeno,Prijmeni,rc,funkce) VALUES ('Petr','Nov·k',7509160439,'z_udr');
INSERT INTO Zamestnanec(Jmeno,Prijmeni,rc,funkce) VALUES ('Michal','Zubrt',8004160109,'z_udr');
INSERT INTO Zamestnanec(Jmeno,Prijmeni,rc,funkce) VALUES ('Alena','Pavlov·',7551020312,'z_pok');
INSERT INTO Zamestnanec(Jmeno,Prijmeni,rc,funkce) VALUES ('EvûÈnie','Kubrov·',8157190107,'z_pok');
INSERT INTO Zamestnanec(Jmeno,Prijmeni,rc,funkce) VALUES ('Karel','Junek',7006120011,'z_vet');
INSERT INTO Zamestnanec(Jmeno,Prijmeni,rc,funkce) VALUES ('David','Kron',7410050879,'z_vet');
INSERT INTO Zamestnanec(Jmeno,Prijmeni,rc,funkce) VALUES ('Lucie','Bordov·',7559100450,'z_vet');
INSERT INTO Zamestnanec(Jmeno,Prijmeni,rc,funkce) VALUES ('Tom·ö','Gerk',7604120436,'z_ose');
INSERT INTO Zamestnanec(Jmeno,Prijmeni,rc,funkce) VALUES ('Radek','Juk',7905240255,'z_ose');
INSERT INTO Zamestnanec(Jmeno,Prijmeni,rc,funkce) VALUES ('Petra','Nov·',8056020126,'z_ose');
INSERT INTO Zamestnanec(Jmeno,Prijmeni,rc,funkce) VALUES ('Bohumil','Vrabec',7012050144,'z_ose');





INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Tereza',to_date('1998-07-10','yyyy-mm-dd'),7604120436);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Romana',to_date('1987-07-08','yyyy-mm-dd'),7604120436);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Tereza',to_date('2000-05-13','yyyy-mm-dd'),7604120436);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Fanouöek',to_date('2001-06-19','yyyy-mm-dd'),7604120436);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('PinÔa',to_date('1992-01-10','yyyy-mm-dd'),7604120436);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Emil',to_date('1998-04-01','yyyy-mm-dd'),7604120436);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('PepÌno',to_date('2001-08-19','yyyy-mm-dd'),7905240255);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Rudolf',to_date('2002-08-17','yyyy-mm-dd'),7905240255);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Miö·',to_date('1983-06-22','yyyy-mm-dd'),7905240255);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Zuzanka',to_date('1984-07-19','yyyy-mm-dd'),7905240255);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('HonzÌk',to_date('2000-04-20','yyyy-mm-dd'),7905240255);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('JaniËka',to_date('1995-06-03','yyyy-mm-dd'),7905240255);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Eliöka',to_date('1997-02-09','yyyy-mm-dd'),8056020126);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('PepÌk',to_date('1980-08-17','yyyy-mm-dd'),8056020126);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Monika',to_date('1980-12-02','yyyy-mm-dd'),8056020126);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('LadÌk',to_date('1986-11-09','yyyy-mm-dd'),8056020126);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Tom',to_date('1979-10-14','yyyy-mm-dd'),8056020126);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Petr',to_date('1980-02-25','yyyy-mm-dd'),8056020126);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Karla',to_date('1981-12-21','yyyy-mm-dd'),7012050144);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('BruËÌk',to_date('1989-09-16','yyyy-mm-dd'),7012050144);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('AlÌk',to_date('2003-01-15','yyyy-mm-dd'),7012050144);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('EviËka',to_date('1999-08-07','yyyy-mm-dd'),7012050144);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Filip',to_date('1997-04-28','yyyy-mm-dd'),7012050144);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('P·ja',to_date('2000-08-15','yyyy-mm-dd'),7012050144);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Ruda',to_date('1980-05-19','yyyy-mm-dd'),7012050144);
INSERT INTO Osetruje(Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES ('Verunka',to_date('2001-09-18','yyyy-mm-dd'),7012050144);


INSERT INTO Vstupenky(cena,typ) VALUES ( 30,'VstupnÈ dÏtskÈ');
INSERT INTO Vstupenky(cena,typ) VALUES ( 30,'VstupnÈ studenskÈ');
INSERT INTO Vstupenky(cena,typ) VALUES ( 60,'VstupnÈ standartnÌ');
INSERT INTO Vstupenky(cena,typ) VALUES ( 150,'VstupnÈ rodinnÈ');

INSERT INTO Prodava(datum_prodeje,Zame_rc,Vstu_typ) VALUES (to_date('2003-12-03 11:30','yyyy-mm-dd hh24:mi'),7551020312,'VstupnÈ dÏtskÈ');
INSERT INTO Prodava(datum_prodeje,Zame_rc,Vstu_typ) VALUES (to_date('2003-10-03 11:45','yyyy-mm-dd hh24:mi'),7551020312,'VstupnÈ dÏtskÈ');
INSERT INTO Prodava(datum_prodeje,Zame_rc,Vstu_typ) VALUES (to_date('2003-12-05 15:50','yyyy-mm-dd hh24:mi'),7551020312,'VstupnÈ standartnÌ');
INSERT INTO Prodava(datum_prodeje,Zame_rc,Vstu_typ) VALUES (to_date('2003-12-09 10:20','yyyy-mm-dd hh24:mi'),8157190107,'VstupnÈ studenskÈ');
INSERT INTO Prodava(datum_prodeje,Zame_rc,Vstu_typ) VALUES (to_date('2003-12-11 9:32','yyyy-mm-dd hh24:mi'),8157190107,'VstupnÈ studenskÈ');
INSERT INTO Prodava(datum_prodeje,Zame_rc,Vstu_typ) VALUES (to_date('2003-12-14 12:45','yyyy-mm-dd hh24:mi'),8157190107,'VstupnÈ rodinnÈ');


INSERT INTO Dodavatel(nazev,adresa,ICO,sortiment) VALUES ('Krmex,s.r.o.','N·b¯eûnÌ 55,Praha 7,170 00',85971210 ,'rostlinn· potrava');
INSERT INTO Dodavatel(nazev,adresa,ICO,sortiment) VALUES ('Zoover a. s.','Torova 189,Praha 9, 198 00',26116839 ,'ûivoËiön· potrava');
INSERT INTO Dodavatel(nazev,adresa,ICO,sortiment) VALUES ('Posdel spol. s r. o.','Redkova 12,Praha 4, 140 00',14598671,'podest˝lka pro zvÌ¯ata');
INSERT INTO Dodavatel(nazev,adresa,ICO,sortiment) VALUES ('Wormex a. s.','VÌznova 45,Praha 1, 110 00',78922633,'propagaËnÌ materi·l');

INSERT INTO Udrzuje(Pavi_c_pav,Zame_rc) VALUES (10,7509160439);
INSERT INTO Udrzuje(Pavi_c_pav,Zame_rc) VALUES (20,7509160439);
INSERT INTO Udrzuje(Pavi_c_pav,Zame_rc) VALUES (30,7509160439);
INSERT INTO Udrzuje(Pavi_c_pav,Zame_rc) VALUES (40,7509160439);
INSERT INTO Udrzuje(Pavi_c_pav,Zame_rc) VALUES (10,8004160109);
INSERT INTO Udrzuje(Pavi_c_pav,Zame_rc) VALUES (20,8004160109);
INSERT INTO Udrzuje(Pavi_c_pav,Zame_rc) VALUES (50,8004160109);


INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2003-10-12','yyyy-mm-dd'),'Tereza',to_date('1998-07-10','yyyy-mm-dd'),7006120011);
INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2002-12-26','yyyy-mm-dd'),'Romana',to_date('1987-07-08','yyyy-mm-dd'),7006120011);
INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2003-09-02','yyyy-mm-dd'),'Tereza',to_date('2000-05-13','yyyy-mm-dd'),7006120011);
INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2003-04-18','yyyy-mm-dd'),'Fanouöek',to_date('2001-06-19','yyyy-mm-dd'),7006120011);
INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2003-02-19','yyyy-mm-dd'),'PinÔa',to_date('1992-01-10','yyyy-mm-dd'),7006120011);
INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2002-11-16','yyyy-mm-dd'),'Emil',to_date('1998-04-01','yyyy-mm-dd'),7410050879);
INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2003-01-05','yyyy-mm-dd'),'PepÌno',to_date('2001-08-19','yyyy-mm-dd'),7410050879);
INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2003-11-19','yyyy-mm-dd'),'Rudolf',to_date('2002-08-17','yyyy-mm-dd'),7410050879);
INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2002-10-09','yyyy-mm-dd'),'Miö·',to_date('1983-06-22','yyyy-mm-dd'),7410050879);
INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2003-05-14','yyyy-mm-dd'),'Zuzanka',to_date('1984-07-19','yyyy-mm-dd'),7410050879);
INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2003-06-02','yyyy-mm-dd'),'HonzÌk',to_date('2000-04-20','yyyy-mm-dd'),7559100450);
INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2003-08-14','yyyy-mm-dd'),'JaniËka',to_date('1995-06-03','yyyy-mm-dd'),7559100450);
INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2001-12-30','yyyy-mm-dd'),'Eliöka',to_date('1997-02-09','yyyy-mm-dd'),7559100450);
INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2003-06-12','yyyy-mm-dd'),'Monika',to_date('1980-12-02','yyyy-mm-dd'),7559100450);
INSERT INTO zdr_prohlidka(datum_prohl,Zvir_jmeno,Zvir_dat_nar,Zame_rc) VALUES (to_date('2003-10-26','yyyy-mm-dd'),'P·ja',to_date('2000-08-15','yyyy-mm-dd'),7559100450);


INSERT INTO Zbozi(c_obj,zbozi,dod_do_ICO,obj_za_rc) VALUES (1,'rostlinnÈ krmnÈ smÏsy',85971210,7604120436);
INSERT INTO Zbozi(c_obj,zbozi,dod_do_ICO,obj_za_rc) VALUES (2,'o¯echy a semÌnka',85971210,7905240255);
INSERT INTO Zbozi(c_obj,zbozi,dod_do_ICO,obj_za_rc) VALUES (3,'drobn˝ hmyz',26116839 ,7905240255);
INSERT INTO Zbozi(c_obj,zbozi,dod_do_ICO,obj_za_rc) VALUES (4,'ovoce',85971210,7604120436);
INSERT INTO Zbozi(c_obj,zbozi,dod_do_ICO,obj_za_rc) VALUES (5,'seno',14598671,8056020126);
INSERT INTO Zbozi(c_obj,zbozi,dod_do_ICO,obj_za_rc) VALUES (6,'reklamnÌ let·ky',78922633,7604120436);
INSERT INTO Zbozi(c_obj,zbozi,dod_do_ICO,obj_za_rc) VALUES (7,'hlodavci',26116839 ,7905240255);
INSERT INTO Zbozi(c_obj,zbozi,dod_do_ICO,obj_za_rc) VALUES (8,'piliny',14598671,8056020126);


COMMIT;
