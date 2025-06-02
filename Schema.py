from pydantic import BaseModel

class guruBase(BaseModel):
    Id_guru : int | None = None
    Nama : str
    Tanggal_lahir :str
    Tempat_lahir : str
    NIK : int
    Agama : str
    email :str
    password : str
    telepon : int
    Alamat :str
    Jabatan : str
    Status_admin : int

class kelasBase(BaseModel):
    Id_kelas : int
    Kelas : str
    Id_wali : int

class jurusanBase(BaseModel):
    Id_jurusan : int
    nama_jurusan : str
    id_kaprodi : int

class SiswaBase(BaseModel):
    Id_siswa : int | None = None
    Nama : str
    Id_jurusan : int
    Id_jurusan : int
    tanggal_lahir : str
    tempat_lahir : str
    NIK : int
    Agama : str
    email : str
    password: str
    telepon : int
    Alamat : str
    status_murid : int

class AdminBase(BaseModel):
    Id_admin : int | None = None
    username : str
    password : str