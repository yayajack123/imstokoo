import pymysql
import time

time.sleep(1)
print("=== ENGINE INTEGRASI TOKO DENGAN BANK ===")
while (1):
    connection_to_bank = 1
    try:
        connToko = pymysql.connect(host='remotemysql.com', user='pvpFOiEYBa', passwd='B3Ycyj91Zv', db='pvpFOiEYBa')
        curToko = connToko.cursor()
    except:
        print("can't connect to TOKO")

    try:
        connBank = pymysql.connect(host='remotemysql.com', user='4QVW7rKZGz', passwd='haWeZTI1cq', db='4QVW7rKZGz')
        curBank = connBank.cursor()
    except:
        print("can't connect to BANK")
        connection_to_bank = 0

    sql_select = "SELECT * FROM tb_invoice"
    curToko.execute(sql_select)
    invoice = curToko.fetchall()

    sql_select = "SELECT * FROM tb_integrasi"
    curToko.execute(sql_select)
    integrasi = curToko.fetchall()

    print("invoice = %d | integrasi = %d" % (len(invoice), len(integrasi)))

# insert listener
    if (len(invoice) > len(integrasi)):
        print("-- INSERT DETECTED --")
        for data in invoice:
            a = 0
        for dataIntegrasi in integrasi:
            if (data[0] == dataIntegrasi[0]):
                a = 1
        if (a == 0):
            print("-- RUN INSERT FOR ID = %s" % (data[0]))
            val = (data[0], data[1], data[2])
            insert_integrasi_toko = "insert into tb_integrasi (id_invoice, total_transaksi, status) values(%s,%s,%s)"
            curToko.execute(insert_integrasi_toko, val)
            connToko.commit()
        if (connection_to_bank == 1):
            insert_integrasi_bank = "insert into tb_integrasi (id_invoice, total_transaksi, status) values(%s,%s,%s)"
            curBank.execute(insert_integrasi_bank, val)
            connBank.commit()
            insert_invoice_bank = "insert into tb_invoice (id_invoice, total_transaksi, status) values(%s,%s,%s)"
            curBank.execute(insert_invoice_bank, val)
            connBank.commit()

    # delete listener
    if (len(invoice) < len(integrasi)):
        print("-- DELETE DETECTED --")
        for dataIntegrasi in integrasi:
            a = 0
            for data in invoice:
                if (dataIntegrasi[0] == data[0]):
                    a = 1
            if (a == 0):
                print("-- RUN DELETE FOR ID = %s" % (dataIntegrasi[0]))
                delete_integrasi_toko = "delete from tb_integrasi where id_invoice = '%s'" % (dataIntegrasi[0])
                curToko.execute(delete_integrasi_toko)
                connToko.commit()
                if (connection_to_bank == 1):
                    delete_integrasi_bank = "delete from tb_integrasi where id_invoice = %s" % (dataIntegrasi[0])
                    curBank.execute(delete_integrasi_bank)
                    connBank.commit()

                    delete_transaksi_bank = "delete from tb_invoice where id_invoice = %s" % (dataIntegrasi[0])
                    curBank.execute(delete_transaksi_bank)
                    connBank.commit()

    # update listener
    if (invoice != integrasi):
        print("-- UPDATE DETECTED --")
        for data in invoice:
            for dataIntegrasi in integrasi:
                if (data[0] == dataIntegrasi[0]):
                    if (data != dataIntegrasi):
                        val = (data[1], data[2], data[0])
                        update_integrasi_toko = "update tb_integrasi set total_transaksi = %s, status = %s where id_invoice = %s"
                        curToko.execute(update_integrasi_toko, val)
                        connToko.commit()
                        if (connection_to_bank == 1):
                            update_integrasi_bank = "update tb_integrasi set total_transaksi = %s, status = %s where id_invoice = %s"
                            curBank.execute(update_integrasi_bank, val)
                            connBank.commit()

                            update_invoice_bank = "update tb_invoice set total_transaksi = %s, status = %s where id_invoice = %s"
                            curBank.execute(update_invoice_bank, val)
                            connBank.commit()
