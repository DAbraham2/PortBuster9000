# Első házifeladat

### Ábrahám Dániel

### DASGYJ

This repository contains all necessary scripts solving the first homework for Network-security course.

All files are marked with an MIT license, are referred by [LICENSE.md](LICENSE.md).

## 1. Megoldás leírása

### 1.1 Port kopogás

A megoldásom megtalálható a solution.buster csomagban.
Azon a gondolaton alapul, hogy a TCP protokoll esetén kapcsolatot kell létesíteni a kliens és a szerver között.

Nem blokkoló utasításokat használok, ezért nem várom meg, hogy a szerver válaszoljon a csatlakozási kérésre.
A próbálkozások során nálam a 400ms-es timeout megszakítás és az 550ms-es várakozás két kérés között megfelelően stabil megoldást eredményezett.
Azaz, a kérés indítása után 400ms után már nem várok válaszra - megszakítom a socket-et.

### 1.2 Csatalkozás

A csatlakozás után megvárom, amíg a szerver üzenetet küld számomra.
Ha érkezik üzenet és ez az elvárt

`Give me your neptun code:`

szöveggel rendelkezik, akkor elküldi a szerver számára a neptunkódomat.
Ha nem sikerült megbizonyosodni, hogy a megfelő szerverrel létesítettem kapcsolatot bontom azt és a program végrehajtása 1-es kóddal véget ér.
Ennek a megoldása is a solution.buster csomagban található.

### 1.3 Matematika

Minden aritmetikához fűződő megoldást a solution.solver.math fájlban található `solve_equations` függvény tarlatmaz.

Itt ismét történik egy ellenőzés, hogy helyesen üzen-e szerver.

A fájl 54. sorában található egy egészen értelmezhetetlen parancs, amivel kinyerem az egyenletek számát.

Minden egyenletet külön felparsolok csupán `int`-ekre és műveletekre.
Mivel a feladatkiírásban csak az összeadás és a kivonás szerepelt, ezért nem készítettem fel más egzotikus művelet végrehajtására.
Az egyenletet a `__solve` függvény oldja meg.

### 1.4 Hash számítás

Ezt a feladatrészt a `solution.taskSolutions` fájl tartalmazza, azon belül pedig a `task_EncryptHash` függvény.

Az eredeti feladatkiírás szerint egyféle módon kérheti a neptn kód és az eredmény összefűzését.
Viszont a tesztelés során néha megállt hibával az a megoldás.

Ezután észrevettem, hogy más formátumban küldi a szerver a `sha('NEPTUN-00000')` üzenetet.

A két variáns a `sha('NEPTUN-00000')` és a `sha('NEPTUN00000')`.

Ezért módosítottam a megoldást, hogy az érkezett üzenet szerinti számolja ki a hash-t.

A hash számításhoz a `pycryptodomex` csomagot használtam.

### 1.5 Hash kiegészítés

A feladatkiírásban szereplő információk alapján nehézkesen tudtam értelmezni az elküldendő információt.
Végülis rájöttem, hogy csak a módosított neptun kód + szám kombinációt kell küldeni.

Ehhez a feladatrészhet tartozó megoldásom a `solution.taskSolutions` csomag `task_SolveExtend` függvényben található.

### 1.6 Web kliens

A fentmaradó megoldások a `solution.taskSolutions.task_navigate_web` függvényben vannak megvalósítva.

Megoldásom lényege, hogy a `requests` csomag segítségével csinálok egy Session-t.
Ebben a session-ben indítok egy `POST` kérést a webszerver felé és a kérés törzsében elhelyezek egy megfelelő
form-data típusú csomagot.

Mivel sessionhöz rendeltem a kérést, ezért nem kell bajlódnom a sütik kezelésével - azok automatikusan hozzá lesznek adva a további kérésekhez.

Ezután a szkript lementi a kliens cert-et és kliens kulcsot a futtató könyvtárba
`clientcert.pem` és `clientkey.pem` néven.

Az első flag kiolvasási kíserlétem után a szerver még kérte, hogy a kérés fejlécébe szerepeljen a

`'User-Agent'-'CrySyS'`,
ezért azt is hozzáillesztettem a kéréshez.

Ezek után már sikeren hajtódott végre a kérés és meg is kaptam a számomra generált egyedi zászlót.

`YouCanHandleNetworking-DASGYJ-44d6bd`

#### További információk a megoldásról:

A futtatás logolva van, ezért keletkezik még egy `debug.log` fájl a futásról.
Ezért viszonylag kevés iformációt ír ki a szkript a konzolra.
Ha valakit érdekel mit is csinál az alkalmazás a logból részletesen kidetül.
A log szintet a `main.py`-ban lehet állítani.

A log és a kliens hitelesítő információk minden futás során újra lesznek generálva, tehát ezek nyugodtan törölhetők a futás előtt.

## 2. Futtatás

The recommended way to run the program is to create a virtual environment
```python -m venv venv```
with at least a **python 3.10**, because the script is relying on type hinting introduced in the 10th version of python3.

After creating the venv, please install all dependencies declared in *requirements.txt* file as follows:

```bash
pip install -r requirements.txt
#Or with
pip3 install -r requirements.txt
```

In the end, the environment is configured and the script could be run in a simple
```python main.py```
From the root folder.