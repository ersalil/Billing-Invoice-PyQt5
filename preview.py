
def run(a, b):
    print(a, "\n",b)
    string = f"""<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet">
    <style>
    table, th, td {{
        border: 1px solid rgb(78, 78, 78);
        border-collapse: collapse;
    }}
        table.center {{
        margin-left: auto;
        margin-right: auto;
    }}
        th, td {{
        padding: 10px;
    }}
        body{{
        margin-top:20px;
        background:#eee;
    }}

    .invoice {{
        background: #fff;
        padding: 20px
    }}

    .invoice-company {{
        font-size: 20px
    }}

    .invoice-header {{
        margin: 0 -20px;
        background: #f0f3f4;
        padding: 20px
    }}

    .invoice-date,
    .invoice-from,
    .invoice-to {{
        display: table-cell;
        width: 1%
    }}

    .invoice-from,
    .invoice-to {{
        padding-right: 20px
    }}

    .invoice-date .date,
    .invoice-from strong,
    .invoice-to strong{{
        font-size: 16px;
        font-weight: 600
    }}

    .invoice-date {{
        text-align: right;
        padding-left: 20px
    }}

    .invoice-price {{
        background: #f0f3f4;
        display: table;
        width: 100%
    }}

    .invoice-price .invoice-price-left,
    .invoice-price .invoice-price-right {{
        display: table-cell;
        padding: 20px;
        font-size: 20px;
        font-weight: 600;
        width: 75%;
        position: relative;
        vertical-align: middle
    }}

    .invoice-price .invoice-price-left .sub-price {{
        display: table-cell;
        vertical-align: middle;
        padding: 0 20px
    }}

    .invoice-price small {{
        font-size: 12px;
        font-weight: 400;
        display: block
    }}

    .invoice-price .invoice-price-row {{
        display: table;
        float: left
    }}

    .invoice-price .invoice-price-right {{
        width: 25%;
        background: #2d353c;
        color: #fff;
        font-size: 28px;
        text-align: right;
        vertical-align: bottom;
        font-weight: 300
    }}

    .invoice-price .invoice-price-right small {{
        display: block;
        opacity: .6;
        position: absolute;
        top: 10px;
        left: 10px;
        font-size: 12px
    }}

    .invoice-footer {{
        border-top: 1px solid #ddd;
        padding-top: 10px;
        font-size: 10px
    }}

    .invoice-note {{
        color: #999;
        margin-top: 80px;
        font-size: 85%
    }}

    .invoice>div:not(.invoice-footer) {{
        margin-bottom: 20px
    }}

    .btn.btn-white, .btn.btn-white.disabled, .btn.btn-white.disabled:focus, .btn.btn-white.disabled:hover, .btn.btn-white[disabled], .btn.btn-white[disabled]:focus, .btn.btn-white[disabled]:hover {{
        color: #2d353c;
        background: #fff;
        border-color: #d9dfe3;
    }}
    </style>
    <div class="container">
    <div class="col-md-12">
        <div class="invoice">
            <div class="invoice-company text-inverse f-w-600">
                AuBasket
            </div>
            <div class="invoice-header">
                <div class="invoice-from">
                <small>from</small>
                <address class="m-t-5 m-b-5">
                    <strong class="text-inverse">AuBasket</strong><br>
                    379, Katewa Nagar<br>
                    Jaipur, 302019<br>
                    Phone: 9887998853<br>
                </address>
                </div>
                <div class="invoice-to">
                <small>to</small>
                <address class="m-t-5 m-b-5">
                    <strong class="text-inverse">{a[2]}</strong><br>
                    Address: {a[4]}<br>
                    Phone: {a[3]}<br>
                    Aadhar No. {a[8]}<br>
                </address>
                </div>
                <div class="invoice-date">
                <small>Invoice Detail</small>
                <div class="date text-inverse m-t-5">Date of Invoice: {a[1]}</div>
                <div class="invoice-detail">
                    Invoice No. #{a[0]}
                </div>
                </div>
            </div>
            <div class="invoice-content">
                <div class="table-responsive">
                <table class="table table-invoice" style="width:100%">
                    <thead>
                        <tr>
                            <th>Item Name</th>
                            <th class="text-center" width="10%">Quantity</th>
                            <th class="text-center" width="10%">Rate / Kg</th>
                            <th class="text-right" width="20%">TOTAL</th>
                        </tr>
                    </thead>
                    <tbody>"""
    string4 = ""                        
    for item in b:
        print(item)
        string4 =  string4 + f"""<tr>
            <td>
            <span class="text-inverse">{item[0]}</span><br>
            </td>
            <td class="text-center">{item[1]}</td>
            <td class="text-center">{item[2]}</td>
            <td class="text-right">{item[3]}</td>
        </tr>"""

    string2 = f""" </tbody>
                </table>
                </div>
                <div class="invoice-price">
                <div class="invoice-price-right">
                    <small>Total Basket</small> <span class="f-w-600">{a[5]}</span>
                </div>
                </div>
            </div>
            <div>
                <p>Payment details: {a[7]}</p>
            </div>
            <div class="invoice-note">
                * Make all cheques payable to AuBasket<br>
                * Payment is due within 30 days<br>
                * If you have any questions concerning this invoice, contact  Salil, tel:+919887998853, mailto:er.salilagrawal@gmail.com
            </div>
            <div class="invoice-footer">
                <p class="text-center m-b-5 f-w-600">
                THANK YOU FOR SHOPPING
                </p>
                <p class="text-center">
                <span class="m-r-10"><i class="fa fa-fw fa-lg fa-globe"></i> <a href="https://www.aubasket.com/" target="_blank" rel="noopener noreferrer">AuBasket.com</a></span>
                <span class="m-r-10"><i class="fa fa-fw fa-lg fa-phone-volume"></i> tel:+919887998853</span>
                <span class="m-r-10"><i class="fa fa-fw fa-lg fa-envelope"></i> mailto:er.salilagrawal@gmail.com</span>
                </p>
            </div>
        </div>
    </div>
    </div>"""

    return string+string4 +string2