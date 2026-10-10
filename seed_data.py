"""一次性填充所有测试数据"""
from app import create_app, db
from app.models import Member, Round, Product, Order

app = create_app()

with app.app_context():
    # 1. 创建协调员账号
    if not Member.query.filter_by(username='ziliang').first():
        coord = Member(username='ziliang', email='z.lu.17@student.scu.edu.au', is_coordinator=True)
        coord.set_password('123456')
        db.session.add(coord)
        print("✅ Created coordinator: ziliang")
    
    # 2. 创建两个普通用户
    for username, email in [('puhao', 'puhao@test.com'), ('yaohan', 'yaohan@test.com')]:
        if not Member.query.filter_by(username=username).first():
            m = Member(username=username, email=email)
            m.set_password('123456')
            db.session.add(m)
            print(f"✅ Created member: {username}")
    
    db.session.commit()
    
    # 3. 创建一个开放的round
    if not Round.query.filter_by(is_open=True).first():
        r = Round(name='Week 42 - October Pickup', is_open=True)
        db.session.add(r)
        db.session.commit()
        print("✅ Created open round: Week 42")
    
    round = Round.query.filter_by(is_open=True).first()
    
    # 4. 添加产品
    products = [
        ('Organic Apples', 4.50, 'kg', 'A1'),
        ('Fresh Bananas', 3.20, 'kg', 'A2'),
        ('Whole Milk', 6.00, 'L', 'B1'),
        ('Sourdough Bread', 7.50, 'loaf', 'C1'),
        ('Free Range Eggs', 8.00, 'dozen', 'B2'),
        ('Oat Milk', 5.50, 'L', 'B3'),
    ]
    
    for name, price, unit, bay in products:
        if not Product.query.filter_by(name=name).first():
            p = Product(name=name, price=price, unit=unit, bay=bay, is_active=True)
            db.session.add(p)
            print(f"✅ Added product: {name}")
    
    db.session.commit()
    
    # 5. 添加订单
    members = Member.query.all()
    products = Product.query.all()
    
    for m in members:
        # 每个人下几个订单
        for i, p in enumerate(products[:3]):
            existing = Order.query.filter_by(member_id=m.id, product_id=p.id, round_id=round.id).first()
            if not existing:
                qty = (i+1) * 2
                o = Order(member_id=m.id, product_id=p.id, round_id=round.id, quantity=qty)
                db.session.add(o)
                print(f"✅ Added order: {m.username} x {p.name} x {qty}")
    
    db.session.commit()
    
    print("\n🎉 所有测试数据填充完成！")
    print("   账号: ziliang / 123456 (协调员)")
    print("   账号: puhao / 123456 (普通用户)")
    print("   账号: yaohan / 123456 (普通用户)")
    print("   开放Round: Week 42 - October Pickup")
    print("   产品: 6个")
    print("   订单: 9个")
