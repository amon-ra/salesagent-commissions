## -*- coding: utf-8 -*-
<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <style type="text/css">
            .overflow_ellipsis {
                text-overflow: ellipsis;
                overflow: hidden;
                white-space: nowrap;
            }

            ${css}

.style-r2 {
    background-color: #efefef;
}
        </style>
    </head>
    <body>

        <%!
        def amount(text):
            return text.replace('-', '&#8209;')  # replace by a non-breaking hyphen (it will not word-wrap between hyphen and numbers)
        %>
        <%
            t_filter = get_filter(data['payment'])
        %>

        <%setLang(user.lang)%>

        <div class="act_as_table data_table">
            <div class="act_as_row labels">
                <div class="act_as_cell">Data</div>
                <div class="act_as_cell">Periodo</div>
                <div class="act_as_cell">Provvigioni</div>
                <div class="act_as_cell">Anno Fiscale</div>
                <div class="act_as_cell"></div>
            </div>
            <div class="act_as_row">
                <div class="act_as_cell">${data['date_from'] and 'DAL' or ''} ${data['date_from'] and formatLang(data['date_from'] or '', date=True) or ''} ${data['date_to'] and 'AL' or ''} ${data['date_from'] and formatLang(data['date_to'] or '', date=True) or ''}</div>
                <div class="act_as_cell">${get_period_range(data['period_ids'])}</div>
                <div class="act_as_cell">${t_filter or ''}</div>
                <div class="act_as_cell">${data['fiscalyear'] or '-' }</div>
                <div class="act_as_cell"><br></div>
            </div>
        </div>

        <% salesagent_id = 0 %>
        <% counter = 0 %>
        <% tot_commission = 0.0 %>
        <% tot_amount_untaxed_commission = 0.0 %>

        %for object in objects:

        %if salesagent_id != object.salesagent_id.id:
          %if salesagent_id:
                      <div class="act_as_row lines labels">
                        <div class="act_as_cell first_column"></div>
                        <div class="act_as_cell"></div>
                        <div class="act_as_cell"><b>Totale</b></div>
                        <div class="act_as_cell amount"><b>${formatLang(tot_amount_untaxed_commission) | amount }</b></div>
                        <div class="act_as_cell amount"><b>${formatLang(tot_commission) | amount }</b></div>
                        %if data['payment'] == 'E':
                            <div class="act_as_cell amount"></div>
                        %endif
                    </div>
                  </div>
              </div>
          </div>
          %endif
          <div class="account_title bg" style="width: 1080px; margin-top: 20px; font-size: 12px;">Agente ${object.salesagent_id and object.salesagent_id.name or ''| entity}</div>

              <div class="act_as_table list_table" style="margin-top: 10px;">

                  <div class="act_as_thead">
                      <div class="act_as_row labels">
                          <div class="act_as_cell first_column" style="width: 140px;">Fattura</div>
                          <div class="act_as_cell" style="width: 260px;">Data Fattura</div>
                          <div class="act_as_cell" style="width: 200px;">Cliente</div>
                          <div class="act_as_cell amount" style="width: 120px;">Imponibile</div>
                          <div class="act_as_cell amount" style="width: 120px;">Provvigioni</div>
                          %if data['payment'] == 'E':
                              <div class="act_as_cell amount" style="width: 120px;">Provvigioni pagate</div>
                          %endif
                      </div>
                  </div>

                  <div class="act_as_tbody">

                      <% counter = 0 %>
                      <% tot_commission = 0.0 %>
                      <% tot_amount_untaxed_commission = 0.0 %>
        %endif
                      <% counter += 1 %>
                      % if counter and (counter % 2) == 0:
                        <% style = "style-r2" %>
                      % else:
                        <% style = "" %>
                      % endif
                      <div class="act_as_row lines">
                          <div class="act_as_cell ${style} first_column">${object.number or ''| entity}</div>
                          <div class="act_as_cell ${style}">${ formatLang(object.date_invoice,date=True) or ''| entity}</div>
                          <div class="act_as_cell ${style}">${object.partner_id and object.partner_id.name or ''| entity}</div>
                          <div class="act_as_cell ${style} amount">${object.amount_untaxed_commission or ''| entity}</div>
                          <div class="act_as_cell ${style} amount">${object.commission or ''| entity}</div>
                          %if data['payment'] == 'E':
                              <div class="act_as_cell ${style} amount">${object.paid_commission and 'PAGATE' or ''| entity}</div>
                          %endif
                      </div>
                      <%
                          tot_commission += object.commission or 0.0
                          tot_amount_untaxed_commission += object.amount_untaxed_commission or 0.0
                      %>
                      <% salesagent_id = object.salesagent_id.id %>



        %endfor
        %if salesagent_id:
                    <div class="act_as_row lines labels">
                      <div class="act_as_cell first_column"></div>
                      <div class="act_as_cell"></div>
                      <div class="act_as_cell"><b>Totale</b></div>
                      <div class="act_as_cell amount"><b>${formatLang(tot_amount_untaxed_commission) | amount }</b></div>
                      <div class="act_as_cell amount"><b>${formatLang(tot_commission) | amount }</b></div>
                      %if data['payment'] == 'E':
                          <div class="act_as_cell amount"></div>
                      %endif
                  </div>
                </div>
            </div>
        </div>
        %endif
    </body>
</html>
