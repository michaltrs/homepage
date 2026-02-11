Drop table Vybeh cascade constraints;
Drop table Pavilon cascade constraints;
Drop table Udrzuje cascade constraints;
Drop table Prodava cascade constraints;
Drop table Vstupenky cascade constraints;
Drop table Osetruje cascade constraints;
Drop table zdr_prohlidka cascade constraints;
Drop table Dodavatel cascade constraints;
Drop table Zamestnanec cascade constraints;
Drop table Zvire cascade constraints;
Drop table Zbozi cascade constraints;
Create table Vybeh (
      nazev VarChar2(50) Null,
      max_zvirat Integer Not Null,
      c_vyb Integer Not Null,
      Pavi_c_pav Integer Not Null,
      Constraint PK_Vybeh Primary Key (c_vyb, Pavi_c_pav)
);
Create table Pavilon (
      nazev VarChar2(40) Not Null,
      c_pav Integer Not Null,
      Constraint PK_Pavilon Primary Key (c_pav)
);
Create table Udrzuje (
      Pavi_c_pav Integer Not Null,
      Zame_rc Integer Not Null,
      Constraint PK_Udrzuje Primary Key (Pavi_c_pav, Zame_rc)
);
Create table Prodava (
      datum_prodeje Date Not Null,
      Vstu_typ VarChar2(40) Not Null,
      Zame_rc Integer Not Null,
      Constraint PK_Prodava Primary Key (datum_prodeje, Vstu_typ, Zame_rc)
);
Create table Vstupenky (
      cena Float Not Null,
      typ VarChar2(40) Not Null,
      Constraint PK_Vstupenky Primary Key (typ)
);
Create table Osetruje (
      Zame_rc Integer Not Null,
      Zvir_jmeno VarChar2(30) Not Null,
      Zvir_dat_nar Date Not Null,
      Constraint PK_Osetruje Primary Key (Zame_rc, Zvir_jmeno, Zvir_dat_nar)
);
Create table zdr_prohlidka (
      datum_prohl Date Not Null,
      Zvir_jmeno VarChar2(30) Not Null,
      Zvir_dat_nar Date Not Null,
      Zame_rc Integer Not Null,
      Constraint PK_zdr_prohlidka Primary Key (datum_prohl, Zvir_jmeno, Zvir_dat_nar, Zame_rc)
);
Create table Dodavatel (
      nazev VarChar2(30) Not Null,
      adresa VarChar2(100) Not Null,
      ICO Integer Not Null,
      sortiment VarChar2(255) Null,
      Constraint PK_Dodavatel Primary Key (ICO)
);
Create table Zamestnanec (
      rc Integer Not Null,
      funkce Char(5) Not Null,
      Prijmeni VarChar2(20) Not Null,
      Jmeno VarChar2(20) Not Null,
      Constraint PK_Zamestnanec Primary Key (rc)
);
Create table Zvire (
      vybeh__c_vyb Integer Not Null,
      vybeh__Pavi_c_pav Integer Not Null,
      dat_nar Date Not Null,
      jmeno VarChar2(30) Not Null,
      nazev VarChar2(30) Not Null,
      frek_krmeni Integer Null,
      puvod VarChar2(60) Null,
      potrava VarChar2(60) Null,
      Constraint PK_Zvire Primary Key (jmeno, dat_nar)
);
Create table Zbozi (
      obj_za_rc Integer Not Null,
      dod_do_ICO Integer Not Null,
      zbozi VarChar2(255) Null,
      c_obj Integer Not Null,
      Constraint PK_Zbozi Primary Key (c_obj)
);
Alter table Vybeh add (
      Constraint FK_Vybeh_1 Foreign Key (Pavi_c_pav) References Pavilon(c_pav)
);
Alter table Udrzuje add (
      Constraint FK_Udrzuje_1 Foreign Key (Pavi_c_pav) References Pavilon(c_pav),
      Constraint FK_Udrzuje_2 Foreign Key (Zame_rc) References Zamestnanec(rc)
);
Alter table Prodava add (
      Constraint FK_Prodava_1 Foreign Key (Vstu_typ) References Vstupenky(typ),
      Constraint FK_Prodava_2 Foreign Key (Zame_rc) References Zamestnanec(rc)
);
Alter table Osetruje add (
      Constraint FK_Osetruje_1 Foreign Key (Zame_rc) References Zamestnanec(rc),
      Constraint FK_Osetruje_2 Foreign Key (Zvir_jmeno, Zvir_dat_nar) References Zvire(jmeno, dat_nar)
);
Alter table zdr_prohlidka add (
      Constraint FK_zdr_prohlidka_1 Foreign Key (Zvir_jmeno, Zvir_dat_nar) References Zvire(jmeno, dat_nar),
      Constraint FK_zdr_prohlidka_2 Foreign Key (Zame_rc) References Zamestnanec(rc)
);
Alter table Zvire add (
      Constraint FK_Zvire_1 Foreign Key (vybeh__c_vyb, vybeh__Pavi_c_pav) References Vybeh(c_vyb, Pavi_c_pav)
);
Alter table Zbozi add (
      Constraint FK_Zbozi_1 Foreign Key (obj_za_rc) References Zamestnanec(rc),
      Constraint FK_Zbozi_2 Foreign Key (dod_do_ICO) References Dodavatel(ICO)
);
