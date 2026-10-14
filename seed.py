"""Sembrador de demostración: usa exclusivamente el contrato HTTP de la API."""
import os, requests
API=os.getenv('API_URL','http://localhost:8000/api/v1'); USER=os.getenv('ADMIN_USERNAME','admin'); PASSWORD=os.getenv('ADMIN_PASSWORD','change-me')
def post(s,path,payload):
    r=s.post(API+path,json=payload); r.raise_for_status(); return r.json()
def main():
    s=requests.Session(); token=post(s,'/login',{'username':USER,'password':PASSWORD})['token']; s.headers['Authorization']=f'Bearer {token}'
    cats= s.get(API+'/categories').json(); books=[]
    for i in range(40): books.append(post(s,'/books',{'title':f'Libro de demostración {i+1:02d}','author':f'Autor {i%10+1}','isbn':f'978000000{i+1:04d}','category_id':cats[i%5]['id'],'total_copies':max(1,i%4+1) }))
    members=[post(s,'/members',{'full_name':f'Socio de demostración {i+1:02d}','document_number':f'DEMO-{i+1:03d}'}) for i in range(10)]
    for i in range(15): post(s,'/loans',{'member_id':members[i%10]['id'],'items':[{'book_id':books[i]['id']}]})
    print(f'Creados: {len(books)} libros, {len(members)} socios y 15 préstamos')
if __name__=='__main__': main()
