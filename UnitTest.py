import unittest
from Login import db,User,app,json
from hashlib import md5

class Testing(unittest.TestCase):

    def setUp(self):
        self.app =app.test_client()
        self.app.testing =True
        db.create_all()
        # db.session.add(User('admin', '123456'))
        # db.session.commit()


        pass

    # def test_insert(self):
    #     result = self.app.get('/insert')
    #     print(result.data)
    #     self.assertEquals(result.status_code,200)
    #     self.assertEquals(result.data.decode(),'Inserted')
    #
    # def test_query(self):
    #     result =self.app.get('/query')
    #     print(result.data)
    #     self.assertEquals(result.status_code,200)
    #     self.assertEquals(result.data.decode(),'123456')

    def test_homepage(self):
        result =self.app.get('/')
        self.assertEquals(result.status_code,302)
        self.assertIn('Redirect',result.data.decode())
        print(result.data)

    def test_login_success(self):
        result = self.app.post('/login', data=dict(
            username='admin',
            password='123456'
        ), follow_redirects=True)

        self.assertEquals(result.status_code,200)
        self.assertIn('This is homepage',result.data.decode())

    def test_login_fail(self):
        result = self.app.post('/login', data=dict(
            username='admin',
            password='123456ajkks'
        ), follow_redirects=True)

        self.assertEquals(result.status_code,200)
        self.assertIn('wrong username or password',result.data.decode())

    def test_register(self):
        result = self.app.post('/register', data=dict(
            username='test6',
            password='123456'
        ), follow_redirects=True)

        user = self.app.get('/query/test6')

        print(user.data)
        self.assertIsNotNone(user)
        self.assertEquals(result.status_code,200)
        self.assertFalse(json.loads(user.data.decode())['password']!=md5('123456'.encode()).hexdigest())

    def tearDown(self):
        # db.drop_all()
        pass

if __name__=='main':
    unittest.main()