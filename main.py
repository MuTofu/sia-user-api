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
async def read_guru(db: db_dependency):
    try:
        guru = db.query(Model.Guru).all()
        return {"code": 200, "message": "Data retrieved successfully", "data": guru}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/siswa/all/", status_code=status.HTTP_200_OK)
async def read_siswa(db: db_dependency):
    try:
        siswa = db.query(Model.Siswa).all()
        return {"code": 200, "message": "Data retrieved successfully", "data": siswa}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/kelas/all/", status_code=status.HTTP_200_OK)
async def read_kelas(db: db_dependency):
    try:
        kelas = db.query(Model.Kelas).all()
        return {"code": 200, "message": "Data retrieved successfully", "data": kelas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jurusan/all/", status_code=status.HTTP_200_OK)
async def read_jurusan(db: db_dependency):
    try:
        jurusan = db.query(Model.Jurusan).all()
        return {"code": 200, "message": "Data retrieved successfully", "data": jurusan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@app.put("/siswa/update/{siswa_id}", status_code=status.HTTP_200_OK)
async def update_siswa(siswa_id: int, siswa: Schema.SiswaBase, db: db_dependency):
    existing_siswa = db.query(Model.Siswa).filter(Model.Siswa.Id_siswa == siswa_id).first()

    if not existing_siswa:
        raise HTTPException(status_code=404, detail="Siswa not found")

    existing_siswa.Nama = siswa.Nama
    existing_siswa.Id_kelas = siswa.Id_kelas
    existing_siswa.Id_jurusan = siswa.Id_jurusan
    existing_siswa.tanggal_lahir = siswa.tanggal_lahir
    existing_siswa.tempat_lahir = siswa.tempat_lahir
    existing_siswa.NIK = siswa.NIK
    existing_siswa.Agama = siswa.Agama
    existing_siswa.email = siswa.email
    existing_siswa.telepon = siswa.telepon
    existing_siswa.password = siswa.password
    existing_siswa.Alamat = siswa.Alamat
    existing_siswa.status_murid = siswa.status_murid

    try:
        db.commit()
        db.refresh(existing_siswa)
        return {"message": "Siswa updated successfully", "data": existing_siswa}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/kelas/update/{kelas_id}", status_code=status.HTTP_200_OK)
async def update_kelas(kelas_id: int, kelas: Schema.kelasBase, db: db_dependency):
    existing_kelas = db.query(Model.Kelas).filter(Model.Kelas.Id_kelas == kelas_id).first()

    if not existing_kelas:
        raise HTTPException(status_code=404, detail="Kelas not found")

    existing_kelas.Kelas = kelas.Kelas
    existing_kelas.Id_wali = kelas.Id_wali

    try:
        db.commit()
        db.refresh(existing_kelas)
        return {"message": "Kelas updated successfully", "data": existing_kelas}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/jurusan/update/{jurusan_id}", status_code=status.HTTP_200_OK)
async def update_jurusan(jurusan_id: int, jurusan: Schema.jurusanBase, db: db_dependency):
    existing_jurusan = db.query(Model.Jurusan).filter(Model.Jurusan.Id_jurusan == jurusan_id).first()

    if not existing_jurusan:
        raise HTTPException(status_code=404, detail="Jurusan not found")

    existing_jurusan.nama_jurusan = jurusan.nama_jurusan
    existing_jurusan.id_kaprodi = jurusan.id_kaprodi

    try:
        db.commit()
        db.refresh(existing_jurusan)
        return {"message": "Jurusan updated successfully", "data": existing_jurusan}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/guru/delete/{guru_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guru(guru_id: int, db: db_dependency):
    existing_guru = db.query(Model.Guru).filter(Model.Guru.Id_guru == guru_id).first()

    if not existing_guru:
        raise HTTPException(status_code=404, detail="Guru not found")

    try:
        db.delete(existing_guru)
        db.commit()
        return {"message": "Guru deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/siswa/delete/{siswa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_siswa(siswa_id: int, db: db_dependency):
    existing_siswa = db.query(Model.Siswa).filter(Model.Siswa.Id_siswa == siswa_id).first()

    if not existing_siswa:
        raise HTTPException(status_code=404, detail="Siswa not found")

    try:
        db.delete(existing_siswa)
        db.commit()
        return {"message": "Siswa deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/kelas/delete/{kelas_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_kelas(kelas_id: int, db: db_dependency):
    existing_kelas = db.query(Model.Kelas).filter(Model.Kelas.Id_kelas == kelas_id).first()

    if not existing_kelas:
        raise HTTPException(status_code=404, detail="Kelas not found")

    try:
        db.delete(existing_kelas)
        db.commit()
        return {"message": "Kelas deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/jurusan/delete/{jurusan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_jurusan(jurusan_id: int, db: db_dependency):
    existing_jurusan = db.query(Model.Jurusan).filter(Model.Jurusan.Id_jurusan == jurusan_id).first()

    if not existing_jurusan:
        raise HTTPException(status_code=404, detail="Jurusan not found")

    try:
        db.delete(existing_jurusan)
        db.commit()
        return {"message": "Jurusan deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login/guru/", status_code=status.HTTP_200_OK)
async def login_guru(guru: Schema.guruLogin, db: db_dependency):
    try:
        existing_guru = db.query(Model.Guru).filter(Model.Guru.email == guru.email).first()
        if not existing_guru or existing_guru.password != guru.password:
            return {"code": 401, "message": "Invalid email or password"}
        else:
            return {"code": 200, "message": "Login successful", "data": existing_guru}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login/siswa/", status_code=status.HTTP_200_OK)
async def login_siswa(siswa: Schema.SiswaBase, db: db_dependency):
    try:
        existing_siswa = db.query(Model.Siswa).filter(Model.Siswa.email == siswa.email).first()
        if not existing_siswa or existing_siswa.password != siswa.password:
            return {"code": 401, "message": "Invalid email or password"}
        else:
            return {"code": 200, "message": "Login successful", "data": existing_siswa}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login/admin/", status_code=status.HTTP_200_OK)
async def login_admin(admin: Schema.AdminBase, db: db_dependency):
    try:
        existing_admin = db.query(Model.Admin).filter(Model.Admin.username == admin.username).first()
        if not existing_admin or existing_admin.password != admin.password:
            return {"code": 401, "message": "Invalid username or password"}
        else:
            return {"code": 200, "message": "Login successful", "data": existing_admin}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))