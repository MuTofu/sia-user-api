from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from Database import Base


class Guru(Base):
    __tablename__ = 'guru'

    Id_guru = Column(Integer, primary_key=True, autoincrement=True)
    Nama = Column(String(100))
    Tanggal_lahir = Column(String(50))
    Tempat_lahir = Column(String(100))
    NIK = Column(Integer)
    Agama = Column(String(10))
    email = Column(String(50))
    password = Column(String(100))
    telepon = Column(Integer)
    Alamat = Column(String(100))
    Jabatan = Column(String(100))
    Status_admin = Column(TINYINT(1))


class Kelas(Base):
    __tablename__ = 'kelas'

    Id_kelas = Column(Integer, primary_key=True)
    Kelas = Column(String(4))
    Id_wali = Column(Integer, ForeignKey("guru.Id_guru"))


class Jurusan(Base):
    __tablename__ = 'jurusan'

    Id_jurusan = Column(Integer, primary_key=True)
    nama_jurusan = Column(String(100))
    id_kaprodi = Column(Integer, ForeignKey("guru.Id_guru"))


class Siswa(Base):
    __tablename__ = 'siswa'

    Id_siswa = Column(Integer, primary_key=True, autoincrement=True)
    Nama = Column(String(100))
    Id_kelas = Column(Integer, ForeignKey("kelas.Id_kelas"))
    Id_jurusan = Column(Integer, ForeignKey("jurusan.Id_jurusan"))
    tanggal_lahir = Column(String(100))
    tempat_lahir = Column(String(100))
    NIK = Column(Integer)
    Agama = Column(String(50))
    email = Column(String(50))
    password = Column(String(100))
    telepon = Column(Integer)
    Alamat = Column(String(100))
    status_murid = Column(TINYINT(1))

class Admin(Base):
    __tablename__ = 'admin'

    Id_admin = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
