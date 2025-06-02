from fastapi import FastAPI, Depends, status, HTTPException
from typing import Annotated
import Model
import Schema
from Database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
Model.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/guru/all/", status_code=status.HTTP_200_OK)
async def read_guru(db : db_dependency):
    guru = db.query(Model.Guru).all()
    respon = {"data" : guru}
    return respon

@app.get("/siswa/all/", status_code=status.HTTP_200_OK)
async def read_siswa(db : db_dependency):
    siswa = db.query(Model.Siswa).all()
    respon = {"data" : siswa}
    return respon

@app.get("/kelas/all/", status_code=status.HTTP_200_OK)
async def read_kelas(db : db_dependency):
    kelas = db.query(Model.Kelas).all()
    respon = {"data" : kelas}
    return respon

@app.get("/jurusan/all/", status_code=status.HTTP_200_OK)
async def read_jurusan(db : db_dependency):
    jurusan = db.query(Model.Jurusan).all()
    respon = {"data" : jurusan}
    return respon


@app.post("/guru/create/", status_code=status.HTTP_201_CREATED)
async def create_guru(guru: Schema.guruBase, db: db_dependency):
    new_guru = Model.Guru(
        Nama=guru.Nama,
        Tanggal_lahir=guru.Tanggal_lahir,
        Tempat_lahir=guru.Tempat_lahir,
        NIK=guru.NIK,
        Agama=guru.Agama,
        email=guru.email,
        telepon=guru.telepon,
        password= guru.password,
        Alamat=guru.Alamat,
        Jabatan=guru.Jabatan,
        Status_admin=guru.Status_admin
    )

    try:
        db.add(new_guru)
        db.commit()
        db.refresh(new_guru)
        return {"message": "Guru created successfully", "data": new_guru}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/siswa/create/", status_code=status.HTTP_201_CREATED)
async def create_siswa(siswa: Schema.SiswaBase, db: db_dependency):
    new_siswa = Model.Siswa(
        Nama=siswa.Nama,
        Id_kelas=siswa.Id_kelas,
        Id_jurusan=siswa.Id_jurusan,
        tanggal_lahir=siswa.tanggal_lahir,
        tempat_lahir=siswa.tempat_lahir,
        NIK=siswa.NIK,
        Agama=siswa.Agama,
        email=siswa.email,
        telepon=siswa.telepon,
        password=siswa.password,
        Alamat=siswa.Alamat,
        status_murid=siswa.status_murid
    )

    try:
        db.add(new_siswa)
        db.commit()
        db.refresh(new_siswa)
        return {"message": "Siswa created successfully", "data": new_siswa}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/kelas/create/", status_code=status.HTTP_201_CREATED)
async def create_kelas(kelas: Schema.kelasBase, db: db_dependency):
    new_kelas = Model.Kelas(
        id_kelas=kelas.Id_kelas,
        Kelas=kelas.Kelas,
        Id_wali=kelas.Id_wali
    )

    try:
        db.add(new_kelas)
        db.commit()
        db.refresh(new_kelas)
        return {"message": "Kelas created successfully", "data": new_kelas}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/jurusan/create/", status_code=status.HTTP_201_CREATED)
async def create_jurusan(jurusan: Schema.jurusanBase, db: db_dependency):
    new_jurusan = Model.Jurusan(
        Id_jurusan=jurusan.Id_jurusan,
        nama_jurusan=jurusan.nama_jurusan,
        id_kaprodi=jurusan.id_kaprodi
    )

    try:
        db.add(new_jurusan)
        db.commit()
        db.refresh(new_jurusan)
        return {"message": "Jurusan created successfully", "data": new_jurusan}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/guru/update/{guru_id}", status_code=status.HTTP_200_OK)
async def update_guru(guru_id: int, guru: Schema.guruBase, db: db_dependency):
    existing_guru = db.query(Model.Guru).filter(Model.Guru.Id_guru == guru_id).first()

    if not existing_guru:
        raise HTTPException(status_code=404, detail="Guru not found")

    existing_guru.Nama = guru.Nama
    existing_guru.Tanggal_lahir = guru.Tanggal_lahir
    existing_guru.Tempat_lahir = guru.Tempat_lahir
    existing_guru.NIK = guru.NIK
    existing_guru.Agama = guru.Agama
    existing_guru.email = guru.email
    existing_guru.telepon = guru.telepon
    existing_guru.password = guru.password
    existing_guru.Alamat = guru.Alamat
    existing_guru.Jabatan = guru.Jabatan
    existing_guru.Status_admin = guru.Status_admin

    try:
        db.commit()
        db.refresh(existing_guru)
        return {"message": "Guru updated successfully", "data": existing_guru}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))