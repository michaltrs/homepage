Drop table Osoba cascade constraints;
Drop table Letadlo cascade constraints;
Drop table Mapa cascade constraints;
Drop table Opravneni_k_instuktazi cascade constraints;
Drop table Opravneni_k_pilotazi cascade constraints;
Drop table Protokol_z_cvicneho_letu cascade constraints;
Drop table Opravneni_k_pilotazi_has_Protokol_z_cvicneho_letu cascade constraints;

Create table Osoba (
	Rodne_cislo VarChar2(10) Not Null,			/* Rodne cislo osoby, pripadne cislo pasu, pro cizince */
	Jmeno VarChar2(45) Not Null,				/* Jmeno osoby */
	Prijmeni VarChar2(45) Not Null,				/* Prijmeni osoby */
	Constraint PK_Osoba Primary Key (Rodne_cislo)
); 

Create table Letadlo (		
	ID Integer Not Null,						/* ID letadla */
	Nazev VarChar2(45) Not Null,				/* Nazev letadla */
	Adresar VarChar2(255) Not Null,				/* Adresar ve kterem se letadlo nachazi */
	Model VarChar2(255) Not Null,				/* Nazev sboru ve kterem je model letadla */
	Datum_vlozeni Date Not Null,				/* Datum kdy bylo letadlo vlozeno*/
	Constraint PK_Letadlo Primary Key (ID)
);

Create table Mapa (
	ID Integer Not Null,						/* ID mapy */
	Nazev VarChar2(45) Not Null,				/* Nazev mapy */
	Adresar VarChar2(255) Not Null,				/* Adresar ve kterem se mapa nachazi */
	Model VarChar2(255) Not Null,				/* Nazev souboru ve kterem je model mapy */
	Datum_vlozeni Date Not Null,				/* Datum kdy byla mapa vlozena */
	Constraint PK_Mapa Primary Key (ID)
);

Create table Opravneni_k_instuktazi (
	Osoba_Rodne_cislo VarChar2(10) Not Null,	/* Drzitel opravneni */
	Letadlo_ID Integer Not Null,				/* Latadlo na ktere se opravneni vztahuje */
	Datum Date Not Null,						/* Datum vystaveni opravneni */
	Constraint PK_Opravneni_k_instuktazi Primary Key (Osoba_Rodne_cislo,Letadlo_ID)
);

Create table Opravneni_k_pilotazi (
	Osoba_Rodne_cislo VarChar2(10) Not Null,	/* Drzitel opravneni */
	Letadlo_ID Integer Not Null,				/* Latadlo na ktere se opravneni vztahuje */
	Datum Date Not Null,						/* Datum vystaveni opravneni */
	Constraint PK_Opravneni_k_pilotazi Primary Key (Osoba_Rodne_cislo,Letadlo_ID)
);

Create table Protokol_z_cvicneho_letu (
	ID Integer Not Null,												/* ID protokolu */
	Mapa_ID Integer Not Null,											/* ID mapy na ktere cviceni probihalo */
	Opravneni_k_instuktazi_Osoba_Rodne_cislo VarChar2(10) Not Null,		/* ID instruktora cviceni */
	Opravneni_k_instuktazi_Letadlo_ID  Integer Not Null,				/* ID letadla ne kterem probihalo cviceni */
	Text_zpravy VarChar2(1000) Null,									/* Protokol o cviceni */
	Datum Date Not Null,												/* Datum cviceni */
	Tema_cvicneho_letu VarChar2(45) Not Null,							/* Tema cviceni */
	Constraint PK_Protokol_z_cvicneho_letu Primary Key (ID)
);

Create table Opravneni_k_pilotazi_has_Protokol_z_cvicneho_letu (
	Opravneni_k_pilotazi_Osoba_Rodne_cislo VarChar2(10) Not Null,		/* ID osoby, ktera se ucastnila cviceni */
	Opravneni_k_pilotazi_Letadlo_ID Integer Not Null,					/* ID letadla na kterem nacvik probihal */
	Protokol_z_cvicneho_letu_ID Integer Not Null,						/* ID protokolu z cviceni */
	Constraint PK_POpravneni_k_pilotazi_has_Protokol_z_cvicneho_letu Primary Key (
		Opravneni_k_pilotazi_Osoba_Rodne_cislo,Opravneni_k_pilotazi_Letadlo_ID,Protokol_z_cvicneho_letu_ID
	)
);

Alter table Opravneni_k_instuktazi add (
      Constraint FK_Opravneni_k_instuktazi_1 Foreign Key (Osoba_Rodne_cislo) References Osoba(Rodne_cislo),
      Constraint FK_Opravneni_k_instuktazi_2 Foreign Key (Letadlo_ID) References Letadlo(ID)
);

Alter table Opravneni_k_pilotazi add (
      Constraint FK_Opravneni_k_pilotazi_1 Foreign Key (Osoba_Rodne_cislo) References Osoba(Rodne_cislo),
      Constraint FK_Opravneni_k_pilotazi_2 Foreign Key (Letadlo_ID) References Letadlo(ID)
);

Alter table Protokol_z_cvicneho_letu add (
      Constraint FK_Protokol_z_cvicneho_letu_1 Foreign Key (Mapa_ID) References Mapa(ID),
      Constraint FK_Protokol_z_cvicneho_letu_2 Foreign Key (Opravneni_k_instuktazi_Osoba_Rodne_cislo) References Opravneni_k_instuktazi(Osoba_Rodne_cislo),
      Constraint FK_Protokol_z_cvicneho_letu_3 Foreign Key (Opravneni_k_instuktazi_Letadlo_ID) References Opravneni_k_instuktazi(Letadlo_ID)
);

Alter table Opravneni_k_pilotazi_has_Protokol_z_cvicneho_letu add (
      Constraint FK_Opravneni_k_pilotazi_has_Protokol_z_cvicneho_letu_1 Foreign Key (Opravneni_k_pilotazi_Osoba_Rodne_cislo) References Opravneni_k_pilotazi(Osoba_Rodne_cislo),
      Constraint FK_Opravneni_k_pilotazi_has_Protokol_z_cvicneho_letu_2 Foreign Key (Opravneni_k_pilotazi_Letadlo_ID) References Opravneni_k_pilotazi(Letadlo_ID),
      Constraint FK_Opravneni_k_pilotazi_has_Protokol_z_cvicneho_letu_3 Foreign Key (Protokol_z_cvicneho_letu_ID) References Protokol_z_cvicneho_letu(ID)
);
