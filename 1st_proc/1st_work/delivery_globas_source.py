
strTmp = '''
<table width="700" align="center" cellpadding="0" cellspacing="0" border="0">
	<tbody><tr><td height="2" colspan="10" class="c1"></td></tr>
	<tr align="center" height="28" class="c2">
		<td width="1" bgcolor="#cccccc"></td>
		<td background="/img/g_mypage_td_title_back.gif" width="66"><font style="font-size:11px;font-family:돋움;">주문종류</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="80"><font style="font-size:11px;font-family:돋움;">주문번호</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="250"><font style="font-size:11px;font-family:돋움;">상품정보</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="100" align="center">
		
		<table width="" height="28" align="center" cellpadding="0" cellspacing="0" border="0">
		<tbody><tr>
			<td align="center"><font style="font-size:11px;font-family:돋움;cursor:hand;cursor:pointer;" onclick="od_status_detail_click_on();">주문상태</font></td>
			<td width="17"><img src="/img/od_status_detail_tbtn.gif" border="0" style="cursor:hand;cursor:pointer;" onclick="od_status_detail_click_on();"></td>
		</tr>
		</tbody></table>
		
		<div id="od_status_detail_div" style="position:absolute;display:none;z-index:1;">
		<table width="120" height="" cellpadding="0" cellspacing="0">
		<tbody><tr>
			<td width="2" height="2" bgcolor="#555555"></td>
			<td width="102" height="2" bgcolor="#555555"></td>
			<td width="14" height="2" bgcolor="#555555"></td>
			<td width="2" height="2" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="14" bgcolor="#555555"></td>
			<td width="102" height="14" bgcolor="#ffffff"></td>
			<td width="14" height="14" bgcolor="#ffffff"><img src="/img/btn_div_close.gif" style="cursor:hand;cursor:pointer;" onclick="od_status_detail_click_off();"></td>
			<td width="2" height="14" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="" bgcolor="#555555"></td>
			<td width="116" height="" colspan="2" bgcolor="#ffffff">

			
			<table width="116" height="" cellpadding="0" cellspacing="0">
			<tbody><tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EC%A3%BC%EB%AC%B8');">주문</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EB%B6%80%EB%B6%84%EC%9E%85%EA%B3%A0');">부분입고</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EB%AA%A8%EB%91%90%EC%9E%85%EA%B3%A0');">모두입고</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%ED%8F%AC%EC%9E%A5%EC%A4%91');">포장중</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%ED%8F%AC%EC%9E%A5%EC%99%84%EB%A3%8C');">포장완료</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B2%B0%EC%A0%9C%EC%99%84%EB%A3%8C');">결제완료</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B5%AD%EC%A0%9C%EB%B0%B0%EC%86%A1%EC%B6%9C%EB%B0%9C%EB%8C%80%EA%B8%B0%EC%A4%91');">국제배송출발대기중</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B5%AD%EC%A0%9C%EB%B0%B0%EC%86%A1%EC%A4%91');">국제배송중</font></td>
			</tr>
			</tbody></table>

			</td>
			<td width="2" height="" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="8" bgcolor="#555555"></td>
			<td width="116" height="8" colspan="2" bgcolor="#ffffff"></td>
			<td width="2" height="8" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="2" bgcolor="#555555"></td>
			<td width="102" height="2" bgcolor="#555555"></td>
			<td width="14" height="2" bgcolor="#555555"></td>
			<td width="2" height="2" bgcolor="#555555"></td>
		</tr>
		</tbody></table>
		</div>
		
		</td>
		<td background="/img/g_mypage_td_title_back.gif" width="50"><font style="font-size:11px;font-family:돋움;">수취인</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="100"><font style="font-size:11px;font-family:돋움;">운송장번호</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="26"><font style="font-size:11px;font-family:돋움;">수취</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="26"><font style="font-size:11px;font-family:돋움;">삭제</font></td>
		<td width="1" bgcolor="#cccccc"></td>
	</tr>

			<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010037" title="귀사 주문번호 : M2430576747QT4"><u><font style="line-height:140%;">2411010037</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010037"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Kniestrumpfe)NORMANI 남성용 노르웨이 무릎 양말 3켤레 매우 두꺼운 플러시 밑창 무연탄 (옵션: /(0)43-46:POLAR HUSKY &amp; GREY,수량:1(옵션가:0) / 옵션: /(0)43-46:POLAR HUSKY &amp; GREY,수량:1(옵션가:0))</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">오창식</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-06"><u>6079055200827</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411010037');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411010037');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010036" title="귀사 주문번호 : M2410311906COX"><u><font style="line-height:140%;">2411010036</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010036"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Miniatures)BMW X5 F15 SUV 회색 2013 1 24 WELLY 모델 자동차 (옵션: (1)OHNE WUNSCHKENNZEICHEN / 옵션: (1)OHNE WUNSCHKENNZEICHEN)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">이성준</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-06"><u>6079055200826</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411010036');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411010036');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010035" title="귀사 주문번호 : D2411011912MK0"><u><font style="line-height:140%;">2411010035</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010035"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Stool Covers)EASNEA 5 X 35CM X 10CM</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김은호</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200825</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411010035');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411010035');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010034" title="귀사 주문번호 : D2411011936FCY"><u><font style="line-height:140%;">2411010034</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010034"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Messenger Bags)YOGCI Leder-Umhängetasche für Herren, Vintage, handgefertigt, Messenger-Tasche, lässige Schultertasche mit magnetischer Schnalle, Klappe über, braun</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김정우</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200824</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411010034');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411010034');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010033" title="귀사 주문번호 : M2411014922WRB"><u><font style="line-height:140%;">2411010033</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010033"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Leg trainer)토구 토팡가 트레이닝 웨이트 스프링 그린 3KG (옵션: (0)WEIGHT TRAINER / 옵션: (0)WEIGHT TRAINER)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">조미주</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-06"><u>6079055200823</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411010033');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411010033');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010029" title="귀사 주문번호 : M2430231332GHJ"><u><font style="line-height:140%;">2411010029</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010029"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">Tommy Hilfiger Correa de Reloj Pulsera 22mm Cuero Marrón - 679301739</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김진옥</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-07"><u>6079055200822</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411010029');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411010029');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010028" title="귀사 주문번호 : D2410301759L0Z"><u><font style="line-height:140%;">2411010028</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010028"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Dedicated Deck Card Games)RAVENSBURGER 23082 - 2 6인용 초콜릿 마녀 가져가기 게임 6세용 컴팩트 포맷 여행 게임 카드 게임 (옵션: (2)SCHOKO HEXE,수량:1(옵션가:0) / 옵션: (2)SCHOKO HEXE,수량:1(옵션가:0))</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김희수</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-05"><u>6079055200821</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411010028');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411010028');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010027" title="귀사 주문번호 : D2410311810NL0"><u><font style="line-height:140%;">2411010027</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010027"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Stands)드럼 음악 및 마이크로 스탠드용 HERCULES 범용 마이크 홀더 클램프</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">기노덕</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-05"><u>6079055200820</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411010027');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411010027');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010026" title="귀사 주문번호 : M24103118330TO"><u><font style="line-height:140%;">2411010026</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010026"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">MyVolts 12 V EU Power Supply Compatible with RME Babyface Pro, Babyface Pro FS, Fireface UCX, Cardbus Audio Interface ((0)NETZTEIL)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">임한별</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200819</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411010026');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411010026');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010024" title="귀사 주문번호 : D2410294608Y0X"><u><font style="line-height:140%;">2411010024</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010024"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Pendants)MATERIA 남성용 목걸이 펜던트 호랑이 검은색 목걸이 40-70CM 보석함 (옵션: (4)INCLUDES 60CM CHAIN,수량:1(옵션가:70380) / 옵션: (4)INCLUDES 60CM CHAIN,수량:1(옵션가:70380))</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">이성웅</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-04"><u>6079055200818</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411010024');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411010024');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411010023" title="귀사 주문번호 : M2430377502C50"><u><font style="line-height:140%;">2411010023</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010023"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Chest &amp; Rib Guards)W WESING Kampfsport Muay Thai Boxen Brust Schutz Sanshou Body Shield - Schwarz - m</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">결제완료</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">이영후</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200817</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411010023');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411010023');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010022" title="귀사 주문번호 : M2430425619Z0K"><u><font style="line-height:140%;">2411010022</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010022"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Drones)홀리스톤 HS360S 드론 프로펠러</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">황선진</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-04"><u>6079055200816</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411010022');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411010022');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010021" title="귀사 주문번호 : M2430434600DQ8"><u><font style="line-height:140%;">2411010021</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010021"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Tyre Pressure Gauges)ATSAFEPRO 타이어 압력 게이지 100PSI 7BAR 정확한 공기 압력 게이지 유연한 튜브 발광 다이얼 자전거 오토바이 자동차 SUV의 슈레이더 밸브용 기계식 타이어 압력 게이지 (옵션: /(1)7BAR &amp; 100PSI,수량:1(옵션가:0) / 옵션: /(1)7BAR &amp; 100PSI,수량:1(옵션가:0))</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">이강윤</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-05"><u>6079055200815</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411010021');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411010021');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010020" title="귀사 주문번호 : M2410301754J2V"><u><font style="line-height:140%;">2411010020</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010020"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Electronic Learning Toys)디티 버드 - 컬러를 만져보세요</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">인한나</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-05"><u>6079055200814</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411010020');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411010020');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010019" title="귀사 주문번호 : M2410304801F84"><u><font style="line-height:140%;">2411010019</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010019"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Bits)4 X SABRECUT SCPSE100 안전 드라이버 비트 크기: 4 6 8 10 X 100 MM(길이)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">장윤석</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-05"><u>6079055200813</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411010019');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411010019');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
			<tr><td colspan="10" height="1" bgcolor="#cccccc"></td></tr>
	</tbody></table>


<table width="700" align="center" cellpadding="0" cellspacing="0" border="0">
	<tbody><tr><td height="2" colspan="10" class="c1"></td></tr>
	<tr align="center" height="28" class="c2">
		<td width="1" bgcolor="#cccccc"></td>
		<td background="/img/g_mypage_td_title_back.gif" width="66"><font style="font-size:11px;font-family:돋움;">주문종류</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="80"><font style="font-size:11px;font-family:돋움;">주문번호</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="250"><font style="font-size:11px;font-family:돋움;">상품정보</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="100" align="center">
		
		<table width="" height="28" align="center" cellpadding="0" cellspacing="0" border="0">
		<tbody><tr>
			<td align="center"><font style="font-size:11px;font-family:돋움;cursor:hand;cursor:pointer;" onclick="od_status_detail_click_on();">주문상태</font></td>
			<td width="17"><img src="/img/od_status_detail_tbtn.gif" border="0" style="cursor:hand;cursor:pointer;" onclick="od_status_detail_click_on();"></td>
		</tr>
		</tbody></table>
		
		<div id="od_status_detail_div" style="position:absolute;display:none;z-index:1;">
		<table width="120" height="" cellpadding="0" cellspacing="0">
		<tbody><tr>
			<td width="2" height="2" bgcolor="#555555"></td>
			<td width="102" height="2" bgcolor="#555555"></td>
			<td width="14" height="2" bgcolor="#555555"></td>
			<td width="2" height="2" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="14" bgcolor="#555555"></td>
			<td width="102" height="14" bgcolor="#ffffff"></td>
			<td width="14" height="14" bgcolor="#ffffff"><img src="/img/btn_div_close.gif" style="cursor:hand;cursor:pointer;" onclick="od_status_detail_click_off();"></td>
			<td width="2" height="14" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="" bgcolor="#555555"></td>
			<td width="116" height="" colspan="2" bgcolor="#ffffff">

			
			<table width="116" height="" cellpadding="0" cellspacing="0">
			<tbody><tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EC%A3%BC%EB%AC%B8');">주문</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EB%B6%80%EB%B6%84%EC%9E%85%EA%B3%A0');">부분입고</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EB%AA%A8%EB%91%90%EC%9E%85%EA%B3%A0');">모두입고</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%ED%8F%AC%EC%9E%A5%EC%A4%91');">포장중</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%ED%8F%AC%EC%9E%A5%EC%99%84%EB%A3%8C');">포장완료</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B2%B0%EC%A0%9C%EC%99%84%EB%A3%8C');">결제완료</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B5%AD%EC%A0%9C%EB%B0%B0%EC%86%A1%EC%B6%9C%EB%B0%9C%EB%8C%80%EA%B8%B0%EC%A4%91');">국제배송출발대기중</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B5%AD%EC%A0%9C%EB%B0%B0%EC%86%A1%EC%A4%91');">국제배송중</font></td>
			</tr>
			</tbody></table>

			</td>
			<td width="2" height="" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="8" bgcolor="#555555"></td>
			<td width="116" height="8" colspan="2" bgcolor="#ffffff"></td>
			<td width="2" height="8" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="2" bgcolor="#555555"></td>
			<td width="102" height="2" bgcolor="#555555"></td>
			<td width="14" height="2" bgcolor="#555555"></td>
			<td width="2" height="2" bgcolor="#555555"></td>
		</tr>
		</tbody></table>
		</div>
		
		</td>
		<td background="/img/g_mypage_td_title_back.gif" width="50"><font style="font-size:11px;font-family:돋움;">수취인</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="100"><font style="font-size:11px;font-family:돋움;">운송장번호</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="26"><font style="font-size:11px;font-family:돋움;">수취</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="26"><font style="font-size:11px;font-family:돋움;">삭제</font></td>
		<td width="1" bgcolor="#cccccc"></td>
	</tr>

			<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040060" title="귀사 주문번호 : M2430709489XTY"><u><font style="line-height:140%;">2411040060</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040060"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">DELPHI SS10562-12B1 Sensor, Drosselklappenstellung Drosselklappensensor, Drosselklappenpotentiometer</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">오석헌</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-08"><u>6079055200861</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411040060');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411040060');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040059" title="귀사 주문번호 : M24307345439HN"><u><font style="line-height:140%;">2411040059</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040059"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Gels)Schwarzkopf Taft Power Gel - V 12 - Tube - 3er Pack (3 x 150ml)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">결제완료</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김해진</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200860</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411040059');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411040059');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040058" title="귀사 주문번호 : M2411022020OHA"><u><font style="line-height:140%;">2411040058</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040058"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">Lifeswonderful - Set of 3 replacement screw in rubber ferrules suitable for Hurrycane Freedom Edition walking sticks체 나사 3개 세트</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김나리</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-08"><u>6079055200859</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411040058');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411040058');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040057" title="귀사 주문번호 : D2411025023UTN"><u><font style="line-height:140%;">2411040057</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040057"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">BRISA VW Collection - Volkswagen Beetle Keyring in Elegant Gift Box with Embossing ( (0)BLUE:EINHEITSGROßE:SINGLE)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">정병화</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-08"><u>6079055200858</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411040057');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411040057');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040056" title="귀사 주문번호 : M2411022008T6U"><u><font style="line-height:140%;">2411040056</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040056"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">PUSTEFIX Magic Bear 180 ml Bubbles Made in Germany Soap Bubbles Toy for Children's Birthday, Wedding, Summer Party &amp; as a Guest Gift Fun for Children and Adults, blue ((1)YELLOW)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">홍태의</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-08"><u>6079055200857</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411040056');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411040056');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040055" title="귀사 주문번호 : M2430781176TPX"><u><font style="line-height:140%;">2411040055</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040055"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Brillenfassungen)Titan Randlose Brillen Runde 48mm Kreis Optische Brillen Rot (: /(2)BREITE DER LINSE：48MM:ROT:1 / /(2)BREITE DER LINSE：48MM:ROT,:1)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">전주희</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200856</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411040055');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411040055');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040054" title="귀사 주문번호 : M2411022005QBH"><u><font style="line-height:140%;">2411040054</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040054"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Stacking &amp; Balancing Games)CAYRO -  ACCION COLORLINE</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">이은경</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200855</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411040054');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411040054');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040053" title="귀사 주문번호 : M2411031958FKT"><u><font style="line-height:140%;">2411040053</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040053"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Stacking &amp; Balancing Games)CAYRO - ACCION COLORLINE </font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">심서연</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200854</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411040053');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411040053');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040052" title="귀사 주문번호 : D24110350239KA"><u><font style="line-height:140%;">2411040052</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040052"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">Gedore 175 Pipe Wrench Swedish Pattern 1 Inch (1 ZOLL,)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">박순영</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-08"><u>6079055200853</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411040052');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411040052');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040051" title="귀사 주문번호 : M2411035036QIL"><u><font style="line-height:140%;">2411040051</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040051"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Stacking &amp; Balancing Games)CAYRO - ACCION COLORLINE</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김기범</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200852</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411040051');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411040051');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040050" title="귀사 주문번호 : M2411042123HEI"><u><font style="line-height:140%;">2411040050</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040050"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">balvi Corkscrew Sardines Colour Blue Bottle Opener in Metal Box Tin</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김태현</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-08"><u>6079055200851</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411040050');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411040050');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040049" title="귀사 주문번호 : M24110451247HZ"><u><font style="line-height:140%;">2411040049</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040049"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">(Postcards)Postkarten-Set Alpen: 9 einzelne Karten (Grußkarten) - Motive aus Bayern Österreich der Schweiz und Italien (Dolomiten/Tirol) Fotos/Bilder/Souvenirs</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">장숙정</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200850</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411040049');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411040049');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040048" title="귀사 주문번호 : M24110421238JC"><u><font style="line-height:140%;">2411040048</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040048"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">Flying into Christmas, Pop and Fiddle Duets for Two Violas, Book One</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김진미</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-08"><u>6079055200849</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411040048');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411040048');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010039" title="귀사 주문번호 : M243057011059L"><u><font style="line-height:140%;">2411010039</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010039"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Signs)스카니아 LED 조명 표지판 60 X 30CM 레이저 조각 우아한 LED 표지판 트럭 액세서리로 사용 가능 USB 또는 12V 및 24V 연결을 위한 조명이 있는 스카니아 로고 표지판 다양한 색상의 트럭 액세서리 (옵션: /(1)USB PORT,수량:1(옵션가:0) / 옵션: /(1)USB PORT,수량:1(옵션가:0))</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">문현민</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-05"><u>6079055200829</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411010039');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411010039');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411010038" title="귀사 주문번호 : M2410314848MZM"><u><font style="line-height:140%;">2411010038</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411010038"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Complete trains)LGB - 70308 Gartenbahn Starterset Weihnachtszug mit Lokomotive und Zwei Waggons, Outdoor-Eisenbahn, Spur G LGB ( (0)SINGLE /  (0)SINGLE)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">윤현호</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200828</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411010038');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411010038');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
			<tr><td colspan="10" height="1" bgcolor="#cccccc"></td></tr>
	</tbody></table>
 
 <table width="700" align="center" cellpadding="0" cellspacing="0" border="0">
	<tbody><tr><td height="2" colspan="10" class="c1"></td></tr>
	<tr align="center" height="28" class="c2">
		<td width="1" bgcolor="#cccccc"></td>
		<td background="/img/g_mypage_td_title_back.gif" width="66"><font style="font-size:11px;font-family:돋움;">주문종류</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="80"><font style="font-size:11px;font-family:돋움;">주문번호</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="250"><font style="font-size:11px;font-family:돋움;">상품정보</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="100" align="center">
		
		<table width="" height="28" align="center" cellpadding="0" cellspacing="0" border="0">
		<tbody><tr>
			<td align="center"><font style="font-size:11px;font-family:돋움;cursor:hand;cursor:pointer;" onclick="od_status_detail_click_on();">주문상태</font></td>
			<td width="17"><img src="/img/od_status_detail_tbtn.gif" border="0" style="cursor:hand;cursor:pointer;" onclick="od_status_detail_click_on();"></td>
		</tr>
		</tbody></table>
		
		<div id="od_status_detail_div" style="position:absolute;display:none;z-index:1;">
		<table width="120" height="" cellpadding="0" cellspacing="0">
		<tbody><tr>
			<td width="2" height="2" bgcolor="#555555"></td>
			<td width="102" height="2" bgcolor="#555555"></td>
			<td width="14" height="2" bgcolor="#555555"></td>
			<td width="2" height="2" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="14" bgcolor="#555555"></td>
			<td width="102" height="14" bgcolor="#ffffff"></td>
			<td width="14" height="14" bgcolor="#ffffff"><img src="/img/btn_div_close.gif" style="cursor:hand;cursor:pointer;" onclick="od_status_detail_click_off();"></td>
			<td width="2" height="14" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="" bgcolor="#555555"></td>
			<td width="116" height="" colspan="2" bgcolor="#ffffff">

			
			<table width="116" height="" cellpadding="0" cellspacing="0">
			<tbody><tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EC%A3%BC%EB%AC%B8');">주문</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EB%B6%80%EB%B6%84%EC%9E%85%EA%B3%A0');">부분입고</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EB%AA%A8%EB%91%90%EC%9E%85%EA%B3%A0');">모두입고</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%ED%8F%AC%EC%9E%A5%EC%A4%91');">포장중</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%ED%8F%AC%EC%9E%A5%EC%99%84%EB%A3%8C');">포장완료</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B2%B0%EC%A0%9C%EC%99%84%EB%A3%8C');">결제완료</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B5%AD%EC%A0%9C%EB%B0%B0%EC%86%A1%EC%B6%9C%EB%B0%9C%EB%8C%80%EA%B8%B0%EC%A4%91');">국제배송출발대기중</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B5%AD%EC%A0%9C%EB%B0%B0%EC%86%A1%EC%A4%91');">국제배송중</font></td>
			</tr>
			</tbody></table>

			</td>
			<td width="2" height="" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="8" bgcolor="#555555"></td>
			<td width="116" height="8" colspan="2" bgcolor="#ffffff"></td>
			<td width="2" height="8" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="2" bgcolor="#555555"></td>
			<td width="102" height="2" bgcolor="#555555"></td>
			<td width="14" height="2" bgcolor="#555555"></td>
			<td width="2" height="2" bgcolor="#555555"></td>
		</tr>
		</tbody></table>
		</div>
		
		</td>
		<td background="/img/g_mypage_td_title_back.gif" width="50"><font style="font-size:11px;font-family:돋움;">수취인</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="100"><font style="font-size:11px;font-family:돋움;">운송장번호</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="26"><font style="font-size:11px;font-family:돋움;">수취</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="26"><font style="font-size:11px;font-family:돋움;">삭제</font></td>
		<td width="1" bgcolor="#cccccc"></td>
	</tr>

			<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411060052" title="귀사 주문번호 : M2431141132G03"><u><font style="line-height:140%;">2411060052</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411060052"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">MamboCat Cazuela Bowl Bruno Tonware I Set of 12 I Diameter 12 cm I Size S I Mediterranean I Glazed I Unique Handmade I Antique/Vintage I Medieval I Viking</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">이지연</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-08"><u>6079055200907</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411060052');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411060052');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411060051" title="귀사 주문번호 : M2411062434YTN"><u><font style="line-height:140%;">2411060051</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411060051"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">(Corkscrew) balvi Corkscrew Sardines Colour Blue Bottle Opener in Metal Box Tin</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">성하룡</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200906</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411060051');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411060051');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411050068" title="귀사 주문번호 : M2411011928IH7"><u><font style="line-height:140%;">2411050068</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411050068"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Mice &amp; Animal Toys)PLAYMONSTER FRAIDY CATS </font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">강주현</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200893</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411050068');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411050068');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411050067" title="귀사 주문번호 : M2430954645KLG"><u><font style="line-height:140%;">2411050067</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411050067"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">MSR (Mountain Safety Research) Kartuschenkocher Pocket Rocket Stove, One size, 6839 ((0)UNBEKANNT:EINHEITSGROßE,)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김용희</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-07"><u>6079055200892</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411050067');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411050067');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411050066" title="귀사 주문번호 : M2411045155LNP"><u><font style="line-height:140%;">2411050066</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411050066"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Stacking &amp; Balancing Games)CAYRO - ACCION COLORLINE </font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김종화</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200891</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411050066');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411050066');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411050065" title="귀사 주문번호 : M2411045156S9Y"><u><font style="line-height:140%;">2411050065</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411050065"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">p4U ALKO Brake Hub Brake Drum Brake 2051 200 x 50 with Bearing Compact Bearing LK 112 x 5 623113 1366103</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김지훈</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-08"><u>6079055200890</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411050065');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411050065');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411050064" title="귀사 주문번호 : D2411045156TBU"><u><font style="line-height:140%;">2411050064</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411050064"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Power Supplies) Cargador ESP Charger Power Supply Adapter 12 V Compatible with Replacement for Guitar Amplifier Vox Mini 3 - Mini 3 G2 Replaces Charging Cable Power Adapter Power Cord Replacement</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">결제완료</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">최혜림</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200889</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411050064');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411050064');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411050063" title="귀사 주문번호 : M2411042201BTI"><u><font style="line-height:140%;">2411050063</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411050063"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Key Rings) F1 Pirelli Motorsport Official Merchandise Keyring with Rubber Wheel Tyre, Hard Tyre, White, White</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">염도현</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-11"><u>6079055200888</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411050063');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411050063');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411050062" title="귀사 주문번호 : D2411055215IIE"><u><font style="line-height:140%;">2411050062</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411050062"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">Schmuckset 925 silber Schneeflocke Halskette mit Anhänger Ohrstecker</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">정세호</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-07"><u>6079055200887</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411050062');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411050062');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411050061" title="귀사 주문번호 : D241105223420X"><u><font style="line-height:140%;">2411050061</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411050061"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Blind rivets)sourcing map 30Stk.Aluminum/Stahl Offenes Ende Blind Nieten 4mm x 40mm</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">안성혁</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200886</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411050061');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411050061');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411050060" title="귀사 주문번호 : M2411055238DXR"><u><font style="line-height:140%;">2411050060</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411050060"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Lint Screens)VHBW WHITE KNIGHT 421309218351 </font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김현경</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-11"><u>6079055200885</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411050060');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411050060');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411050059" title="귀사 주문번호 : D2431057676ANG"><u><font style="line-height:140%;">2411050059</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411050059"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">Ultnice 200 round glass mosaic tiles, mixed mosaic glass pieces for DIY craft, jewellery making, 10 mm, pack of 200</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
				<tr><td width="250" height="1" background="/img/dot_line.gif"></td></tr>
				<tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411050059"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">ULTNICE 200 stücke Runde Glasmosaik Fliesen Mixed Mosaik Glas Stücke für DIY Handwerk Schmuck Machen 14mm</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">노대일</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-07"><u>6079055200884</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411050059');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411050059');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040063" title="귀사 주문번호 : M2430638905S20"><u><font style="line-height:140%;">2411040063</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040063"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">eco:fy Awnings and Parasol Waterproofing Spray Sun Shade Protection Against Moisture and Dirt UV-Stable (0.5 Litres) ( /(1)2 | 5 LITER(+25,636),)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">홍태만</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-08"><u>6079055200864</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411040063');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411040063');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040062" title="귀사 주문번호 : M2430666646STK"><u><font style="line-height:140%;">2411040062</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040062"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">Stanley Fatmax Gen1 SFMCB100 Adapter (for Operating the Existing Range (First Stanley Fatmax Devices) with the V20 System , Not Included</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">이종철</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-08"><u>6079055200863</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411040062');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411040062');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411040061" title="귀사 주문번호 : M2411014917FKS"><u><font style="line-height:140%;">2411040061</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411040061"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Sheets)GOPLNMA - Goplnma-Anime Bettwäsche-Set, Bettbezug Anime, 3D Druck,mit Kissenbezug,Für Kinder Erwachsene,Für Einzelbett Doppelbett ( (17)220×240CM:1 / (17)220×240CM:1)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김지은</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200862</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411040061');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411040061');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
			<tr><td colspan="10" height="1" bgcolor="#cccccc"></td></tr>
	</tbody></table>
 
 <table width="700" align="center" cellpadding="0" cellspacing="0" border="0">
	<tbody><tr><td height="2" colspan="10" class="c1"></td></tr>
	<tr align="center" height="28" class="c2">
		<td width="1" bgcolor="#cccccc"></td>
		<td background="/img/g_mypage_td_title_back.gif" width="66"><font style="font-size:11px;font-family:돋움;">주문종류</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="80"><font style="font-size:11px;font-family:돋움;">주문번호</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="250"><font style="font-size:11px;font-family:돋움;">상품정보</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="100" align="center">
		
		<table width="" height="28" align="center" cellpadding="0" cellspacing="0" border="0">
		<tbody><tr>
			<td align="center"><font style="font-size:11px;font-family:돋움;cursor:hand;cursor:pointer;" onclick="od_status_detail_click_on();">주문상태</font></td>
			<td width="17"><img src="/img/od_status_detail_tbtn.gif" border="0" style="cursor:hand;cursor:pointer;" onclick="od_status_detail_click_on();"></td>
		</tr>
		</tbody></table>
		
		<div id="od_status_detail_div" style="position:absolute;display:none;z-index:1;">
		<table width="120" height="" cellpadding="0" cellspacing="0">
		<tbody><tr>
			<td width="2" height="2" bgcolor="#555555"></td>
			<td width="102" height="2" bgcolor="#555555"></td>
			<td width="14" height="2" bgcolor="#555555"></td>
			<td width="2" height="2" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="14" bgcolor="#555555"></td>
			<td width="102" height="14" bgcolor="#ffffff"></td>
			<td width="14" height="14" bgcolor="#ffffff"><img src="/img/btn_div_close.gif" style="cursor:hand;cursor:pointer;" onclick="od_status_detail_click_off();"></td>
			<td width="2" height="14" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="" bgcolor="#555555"></td>
			<td width="116" height="" colspan="2" bgcolor="#ffffff">

			
			<table width="116" height="" cellpadding="0" cellspacing="0">
			<tbody><tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EC%A3%BC%EB%AC%B8');">주문</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EB%B6%80%EB%B6%84%EC%9E%85%EA%B3%A0');">부분입고</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EB%AA%A8%EB%91%90%EC%9E%85%EA%B3%A0');">모두입고</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%ED%8F%AC%EC%9E%A5%EC%A4%91');">포장중</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%ED%8F%AC%EC%9E%A5%EC%99%84%EB%A3%8C');">포장완료</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B2%B0%EC%A0%9C%EC%99%84%EB%A3%8C');">결제완료</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B5%AD%EC%A0%9C%EB%B0%B0%EC%86%A1%EC%B6%9C%EB%B0%9C%EB%8C%80%EA%B8%B0%EC%A4%91');">국제배송출발대기중</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B5%AD%EC%A0%9C%EB%B0%B0%EC%86%A1%EC%A4%91');">국제배송중</font></td>
			</tr>
			</tbody></table>

			</td>
			<td width="2" height="" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="8" bgcolor="#555555"></td>
			<td width="116" height="8" colspan="2" bgcolor="#ffffff"></td>
			<td width="2" height="8" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="2" bgcolor="#555555"></td>
			<td width="102" height="2" bgcolor="#555555"></td>
			<td width="14" height="2" bgcolor="#555555"></td>
			<td width="2" height="2" bgcolor="#555555"></td>
		</tr>
		</tbody></table>
		</div>
		
		</td>
		<td background="/img/g_mypage_td_title_back.gif" width="50"><font style="font-size:11px;font-family:돋움;">수취인</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="100"><font style="font-size:11px;font-family:돋움;">운송장번호</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="26"><font style="font-size:11px;font-family:돋움;">수취</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="26"><font style="font-size:11px;font-family:돋움;">삭제</font></td>
		<td width="1" bgcolor="#cccccc"></td>
	</tr>

			<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411080053" title="귀사 주문번호 : D2411082555TG0"><u><font style="line-height:140%;">2411080053</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411080053"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Underbeds &amp; mattress savers)BEURER UB 90 Comfortable Heated Under Blanket Warm and cozy under blanket with 2 separately adjustable temperature zones ((2)ZWEI TEMPERATURZONEN + 9 TEMPERATURSTUFEN,(24956) / (2)ZWEI TEMPERATURZONEN + 9 TEMPERATURSTUFEN,(:24</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">결제완료</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">송은령</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200930</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411080053');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411080053');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411080052" title="귀사 주문번호 : M2411082556CNR"><u><font style="line-height:140%;">2411080052</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411080052"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">(Emblems)Steering wheel Volvo original emblem sign logo airbag V40 S60 V60 XC60 V70 XC70 S80</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김기운</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200929</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411080052');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411080052');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411070031" title="귀사 주문번호 : D2411062436SLJ"><u><font style="line-height:140%;">2411070031</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411070031"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Pack Covers)FJALLRAVEN UNI KANKEN  ((0)40:BLACK / (0)40:BLACK)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">최준</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200922</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411070031');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411070031');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411070030" title="귀사 주문번호 : D2411065436WMS"><u><font style="line-height:140%;">2411070030</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411070030"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(LED lamps) OSRAM BASE LED PIN Bulb with G9 Socket, 2.60 W, Replacement for 30 W Incandescent Bulb, Warm White (2700 K), Pack of 3 ((2)30W REPLACEMENT:3 STUCK (1ER PACK):NOT DIMMABLE / (2)30W REPLACEMENT:3 STUCK (1ER PACK):NOT DIMMABLE)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">모두입고</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">민규암</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200921</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411070030');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411070030');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411070029" title="귀사 주문번호 : M2411065436ZMV"><u><font style="line-height:140%;">2411070029</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411070029"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Submersible)BARWIG  Barwig Heavyweight Submersible Pump - 18 Litres</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김종삼</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-11"><u>6079055200920</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411070029');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411070029');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411070028" title="귀사 주문번호 : M2411075416VV8"><u><font style="line-height:140%;">2411070028</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411070028"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Windschotts) GermanTuningParts Wind Deflector for Mercedes A207 - Folding - with Quick Release - Black | Wind Deflector | Wind Deflector</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">장예찬</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-11"><u>6079055200919</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411070028');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411070028');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411070027" title="귀사 주문번호 : M2411075440C6B"><u><font style="line-height:140%;">2411070027</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411070027"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Gels)SCHWARZKOPF TAFT - Taft Maxx Power Hair Styling Gel Pack of 6 (6 x 300 ml) Buy it again</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">염성현</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-11"><u>6079055200918</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411070027');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411070027');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411070026" title="귀사 주문번호 : D2411075432FTD"><u><font style="line-height:140%;">2411070026</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411070026"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Bars) Flexi-Bar Athletic, Black, Heavy Duty Swing Rod by Flexi-Sports with Introduction DVD and Training Plan, Swing Stick Buy it again</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">결제완료</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">성시헌</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200917</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411070026');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411070026');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411070025" title="귀사 주문번호 : M2411072438KEK"><u><font style="line-height:140%;">2411070025</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411070025"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Bags Cases &amp; Racks)DECKSAVER NUMARK MIXTRACK PLATINUM FX PRO FX </font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">신필경</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-11"><u>6079055200916</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411070025');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411070025');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411070024" title="귀사 주문번호 : D2411075438OME"><u><font style="line-height:140%;">2411070024</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411070024"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Dishes) Homecraft Newstead Cutlery, Left Handed Fork (Eligible for VAT relief in the UK) Adaptive Dining Aid, Utensil for Elderly, Disabled, Parkinson's Disease, and Arthritis, Eat Easier, Non-Slip Grip Buy it again</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">결제완료</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">전현재</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200915</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411070024');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411070024');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411070023" title="귀사 주문번호 : D2411075456LYK"><u><font style="line-height:140%;">2411070023</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411070023"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;"> UV-Marker Securitas e-8280, Rundspitze 1,5-3mm, farblos Buy it again (옵션: (0)1:UV MARKER / 옵션: (0)1:UV MARKER)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">안치현</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200914</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411070023');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411070023');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411070022" title="귀사 주문번호 : M24110725003SD"><u><font style="line-height:140%;">2411070022</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411070022"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">(Wrist Watches)BERGMANN -  Watch model 1922, Silver case, Strap. Buy it again</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">유동훈</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200913</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411070022');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411070022');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411060055" title="귀사 주문번호 : D2411055310KEN"><u><font style="line-height:140%;">2411060055</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411060055"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">Cubilux Passive Audio Switcher, Bi-Directional 1 to 4 6.35 mm TRS Jack Speaker Switch, 4-Channel Stereo Aux Switch Selector for Headphones Sound System Amplifier</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">고대한</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-08"><u>6079055200910</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411060055');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411060055');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411060054" title="귀사 주문번호 : M2431075935F3O"><u><font style="line-height:140%;">2411060054</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411060054"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Stacking &amp; Balancing Games)CAYRO - ACCION COLORLINE </font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">모두입고</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">노은지</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200909</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411060054');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411060054');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411060053" title="귀사 주문번호 : M24110623559X9"><u><font style="line-height:140%;">2411060053</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411060053"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">Dyceittdia Protein Hair Straightening Cream, 100 ml, Silk and Shine Hair Straightening Cream, Straightening Cream for Curly Hair, Suitable for All Hair Types</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">국제배송중</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">백인철</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 2024-11-08"><u>6079055200908</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_com_click('on', '2411060053');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411060053');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
			<tr><td colspan="10" height="1" bgcolor="#cccccc"></td></tr>
	</tbody></table>
 
 <table width="700" align="center" cellpadding="0" cellspacing="0" border="0">
	<tbody><tr><td height="2" colspan="10" class="c1"></td></tr>
	<tr align="center" height="28" class="c2">
		<td width="1" bgcolor="#cccccc"></td>
		<td background="/img/g_mypage_td_title_back.gif" width="66"><font style="font-size:11px;font-family:돋움;">주문종류</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="80"><font style="font-size:11px;font-family:돋움;">주문번호</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="250"><font style="font-size:11px;font-family:돋움;">상품정보</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="100" align="center">
		
		<table width="" height="28" align="center" cellpadding="0" cellspacing="0" border="0">
		<tbody><tr>
			<td align="center"><font style="font-size:11px;font-family:돋움;cursor:hand;cursor:pointer;" onclick="od_status_detail_click_on();">주문상태</font></td>
			<td width="17"><img src="/img/od_status_detail_tbtn.gif" border="0" style="cursor:hand;cursor:pointer;" onclick="od_status_detail_click_on();"></td>
		</tr>
		</tbody></table>
		
		<div id="od_status_detail_div" style="position:absolute;display:none;z-index:1;">
		<table width="120" height="" cellpadding="0" cellspacing="0">
		<tbody><tr>
			<td width="2" height="2" bgcolor="#555555"></td>
			<td width="102" height="2" bgcolor="#555555"></td>
			<td width="14" height="2" bgcolor="#555555"></td>
			<td width="2" height="2" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="14" bgcolor="#555555"></td>
			<td width="102" height="14" bgcolor="#ffffff"></td>
			<td width="14" height="14" bgcolor="#ffffff"><img src="/img/btn_div_close.gif" style="cursor:hand;cursor:pointer;" onclick="od_status_detail_click_off();"></td>
			<td width="2" height="14" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="" bgcolor="#555555"></td>
			<td width="116" height="" colspan="2" bgcolor="#ffffff">

			
			<table width="116" height="" cellpadding="0" cellspacing="0">
			<tbody><tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EC%A3%BC%EB%AC%B8');">주문</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EB%B6%80%EB%B6%84%EC%9E%85%EA%B3%A0');">부분입고</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EB%AA%A8%EB%91%90%EC%9E%85%EA%B3%A0');">모두입고</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%ED%8F%AC%EC%9E%A5%EC%A4%91');">포장중</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%ED%8F%AC%EC%9E%A5%EC%99%84%EB%A3%8C');">포장완료</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B2%B0%EC%A0%9C%EC%99%84%EB%A3%8C');">결제완료</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B5%AD%EC%A0%9C%EB%B0%B0%EC%86%A1%EC%B6%9C%EB%B0%9C%EB%8C%80%EA%B8%B0%EC%A4%91');">국제배송출발대기중</font></td>
			</tr>
			<tr>
				<td width="116" height="22" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;cursor:hand;cursor:pointer;" onclick="od_status_detaile_val_click('%EA%B5%AD%EC%A0%9C%EB%B0%B0%EC%86%A1%EC%A4%91');">국제배송중</font></td>
			</tr>
			</tbody></table>

			</td>
			<td width="2" height="" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="8" bgcolor="#555555"></td>
			<td width="116" height="8" colspan="2" bgcolor="#ffffff"></td>
			<td width="2" height="8" bgcolor="#555555"></td>
		</tr>
		<tr>
			<td width="2" height="2" bgcolor="#555555"></td>
			<td width="102" height="2" bgcolor="#555555"></td>
			<td width="14" height="2" bgcolor="#555555"></td>
			<td width="2" height="2" bgcolor="#555555"></td>
		</tr>
		</tbody></table>
		</div>
		
		</td>
		<td background="/img/g_mypage_td_title_back.gif" width="50"><font style="font-size:11px;font-family:돋움;">수취인</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="100"><font style="font-size:11px;font-family:돋움;">운송장번호</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="26"><font style="font-size:11px;font-family:돋움;">수취</font></td>
		<td background="/img/g_mypage_td_title_back.gif" width="26"><font style="font-size:11px;font-family:돋움;">삭제</font></td>
		<td width="1" bgcolor="#cccccc"></td>
	</tr>

			<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411110053" title="귀사 주문번호 : M2411092624A7C"><u><font style="line-height:140%;">2411110053</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411110053"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">(Foot Creams)Neutrogena Norwegian Formula Foot Cream Nordic Berry 1 X 100 ML</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">육현옥</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200961</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411110053');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411110053');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411110052" title="귀사 주문번호 : M2411102616YHI"><u><font style="line-height:140%;">2411110052</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411110052"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">(Cutter &amp; Accessories)CREDO 1854 Smart Cutter Replacement Clips Pack of 2</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김종현</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200960</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411110052');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411110052');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411110051" title="귀사 주문번호 : M2411102618UAB"><u><font style="line-height:140%;">2411110051</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411110051"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">(Bed Pillows)Ergonomically washable reading bone - Made in Germany: Meditation pillow Relaxation pillow Neck pillow - Supports books Tablet smartphone Mobile phone - Organic Half Linen Dandelion Linen Natural</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">배슬아</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200959</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411110051');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411110051');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411110050" title="귀사 주문번호 : M2411102620OCB"><u><font style="line-height:140%;">2411110050</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411110050"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">(Bed Pillows)Ergonomic Washable Reading Bone - Made in Germany - Meditation Cushion Relaxation Cushion Neck Pillow - Book Tablet Smartphone Mobile Phone Support - Organic Half Linen Dandelion Purple</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">배슬아</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200958</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411110050');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411110050');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411110049" title="귀사 주문번호 : M2431568521SCO"><u><font style="line-height:140%;">2411110049</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411110049"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">(Sewing)AVENIR CH1625 Mixed Unicorn Deer Plush (/(0)DEER,:1 / /(0)DEER,1)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">박준철</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200957</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411110049');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411110049');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411110048" title="귀사 주문번호 : M24316358548IJ"><u><font style="line-height:140%;">2411110048</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411110048"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">(Back massage)LYAPKO AALP CHANCE 6 2 Massage Mat</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">안혜진</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200956</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411110048');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411110048');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411110047" title="귀사 주문번호 : D24111127018IX"><u><font style="line-height:140%;">2411110047</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411110047"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">(Doors)SPARES2GO Door Hinge Set for Built-in Refrigerators and Freezers (Left and Right Hinges with Code: 3306 3702 3307 3703 5.0 41.5)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">채규섭</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200955</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411110047');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411110047');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411110046" title="귀사 주문번호 : M2411112715XQH"><u><font style="line-height:140%;">2411110046</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411110046"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">(Peristaltic dosing pumps)Dosing pump hose pump PVG 230V adjustable 8.0-20.0 LH operation indicator</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김도형</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200954</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411110046');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411110046');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
						
			<a href="./orderinquiryview.php?od_id=2411110045" title="귀사 주문번호 : M2431653378FJG"><u><font style="line-height:140%;">2411110045</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411110045"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">(Light bulbs)2 Pack BA15S 18W 32V Dimmable 27</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김국환</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200953</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411110045');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411110045');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411080059" title="귀사 주문번호 : D2411075500KJX"><u><font style="line-height:140%;">2411080059</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411080059"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Band Saw Accessories)HEGNER 00000100-2 Saw Blade Clamp Square Screw Slot Width 0.7MM Pack of 2</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">결제완료</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">김성경</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200936</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411080059');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411080059');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411080058" title="귀사 주문번호 : M2431270079JU3"><u><font style="line-height:140%;">2411080058</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411080058"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#555555;font-weight:;">(Nail Care)Nail Polish 10ML to prevent nail biting for children</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">주문</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">황국화</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200935</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411080058');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_on.gif" border="0" title="" style="cursor:hand;cursor:pointer;" onclick="od_del_click('on', '2411080058');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411080057" title="귀사 주문번호 : M2411082457WNI"><u><font style="line-height:140%;">2411080057</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411080057"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Hand-brown)KES Shower Rail Stainless Steel SUS 304 Wall Rail Shower Head Holder Adjustable Bar Shower Head 100 CM Long Glossy F209S100-PS ((0)78 CM:BRUSHED / (0)78 CM:BRUSHED)</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">결제완료</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">이용구</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200934</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411080057');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411080057');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411080056" title="귀사 주문번호 : M24110855195XG"><u><font style="line-height:140%;">2411080056</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411080056"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Discs)BESTPRICE 2 X Rear Brake Disc Diameter 305 MM Fully Compatible NISSAN NV400 (X62 X62B) OPEL MOVANO B (X62) RENAULT MAS</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">결제완료</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">박근영</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200933</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411080056');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411080056');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411080055" title="귀사 주문번호 : M2411082537QNB"><u><font style="line-height:140%;">2411080055</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411080055"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Tambourines)FLEXZION Tambourine Hand Drum - 25CM Bell Garland Handle Music Percussion Instrument Crescent Shape Frame 2 Rows Bell Ring Metal Jingle for KTV and Party White 20 Pairs ((1)GRUN(0) / (1)GRUN(0))</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">결제완료</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">이나윤</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200932</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411080055');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411080055');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
		<tr><td colspan="10" height="1" bgcolor="#dddddd"></td></tr>
		<tr>
			<td width="1" bgcolor="#cccccc"></td>
			<td width="66" height="30" align="center" valign="middle"><img src="/img/orderinquiry_shipping_icon.gif" border="0"></td> 

			
			<td width="80" height="30" align="center" style="word-break:break-all;">
			
							<div id="order_dialog_new_div" style="position:absolute;display:;z-index:1;">
				<table width="18" height="9" cellpadding="0" cellspacing="0">
				<tbody><tr>
					<td width="18" height="9"><img src="/img/order_dialog_new_img.gif" border="0"></td>
				</tr>
				</tbody></table>
				</div>
						
			<a href="./orderinquiryview.php?od_id=2411080054" title="귀사 주문번호 : D24313469027ZB"><u><font style="line-height:140%;">2411080054</font></u></a></td>
			<td width="250" height="30" align="left" valign="middle" style="word-break:break-all;">

			<table width="250" height="40" align="left" cellpadding="0" cellspacing="0">

			
				
				<tbody><tr><td width="250" height="10"></td></tr>
				<tr>
					<td width="250" height="20" style="word-break:break-all;"><a href="./orderinquiryview.php?od_id=2411080054"><font style="font-size:11px;font-family:돋움;line-height:13px;color:#387fb8;font-weight:bold;">(Liquid Ink Rollerball Pens)UNI-BALL UB200 VISION ELITE INK ROLLER PEN 0.8MM TIP 0.6MM LINE WIDTH 12 BLACK</font></a></td>
				</tr>
				<tr><td width="250" height="10"></td></tr>

				
			</tbody></table>

			</td>
			<td width="100" height="30" align="center"><font style="font-family:돋움;font-size:11px;color:#555555;">결제완료</font></td>
			<td width="50" height="30" align="center" style="word-break:break-all;"><font style="font-family:돋움;font-size:11px;color:#555555;">박현규</font></td>
							<td width="100" height="30" align="center"><font style="font-size:12px;font-family:돋움;color:#555555"><a href="http://expressweb.co.kr/enha" target="_blank" title="출발일 : 0000-00-00"><u>6079055200931</u></a></font></td>
						<td width="26" height="30" align="center"><img src="/img/btn_com_off.gif" border="0" title="아직 수취 완료할 수 없는 주문입니다." style="cursor:hand;cursor:pointer;" onclick="od_com_click('off', '2411080054');"></td>
			<td width="26" height="30" align="center"><img src="/img/btn_del_off.gif" border="0" title="진행 중인 주문서는 삭제할 수 없습니다." style="cursor:hand;cursor:pointer;" onclick="od_del_click('off', '2411080054');"></td>
			<td width="1" bgcolor="#cccccc"></td>
		</tr>
			<tr><td colspan="10" height="1" bgcolor="#cccccc"></td></tr>
	</tbody></table>
 
 
'''