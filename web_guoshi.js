// const { randomInt } = require("firebase-tools/lib/utils");

function helloword() {
    console.log("Hello World");
}

window.helloword = helloword;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function preventAFK() {
	if (typeof GameMgr == 'undefined') {
		return;
	}
	GameMgr.Inst._pre_mouse_point.x = Math.floor(Math.random() * 100) + 1;
	GameMgr.Inst._pre_mouse_point.y = Math.floor(Math.random() * 100) + 1;
	GameMgr.Inst.clientHeatBeat(); // Prevent Client-side AFK
	app.NetAgent.sendReq2Lobby('Lobby', 'heatbeat', { no_operation_counter: 0 }); //Prevent Server-side AFK

	if (typeof view == 'undefined' || typeof view.DesktopMgr == 'undefined' ||
		typeof view.DesktopMgr.Inst == 'undefined' || view.DesktopMgr.Inst == null) {
		return;
	}
	view.DesktopMgr.Inst.hangupCount = 0;
	//uiscript.UI_Hangup_Warn.Inst.locking
}

setInterval(preventAFK, 30000);

// MajSoul specific functions

function makeCall(type) {
	app.NetAgent.sendReq2MJ('FastTest', 'inputChiPengGang', { type: type, index: 0, timeuse: Math.random() * 2 + 1 });
	view.DesktopMgr.Inst.WhenDoOperation();
}

function getOperations() {
	return mjcore.E_PlayOperation;
}

function getDora() {
	return view.DesktopMgr.Inst.dora;
}

function getPlayerHand() {
	return view.DesktopMgr.Inst.players[0].hand;
}

function doesPlayerExist(player) {
	return typeof view.DesktopMgr.Inst.players[player].hand != 'undefined' && view.DesktopMgr.Inst.players[player].hand != null;
}

function declineCall(operation) {
	try {
		if (operation == getOperationList()[getOperationList().length - 1].type) { //Is last operation -> Send decline Command
			app.NetAgent.sendReq2MJ('FastTest', 'inputChiPengGang', { cancel_operation: true, timeuse: 2 });
			view.DesktopMgr.Inst.WhenDoOperation();
		}
	}
	catch {
		log("Failed to decline the Call. Maybe someone else was faster?");
	}
}

//Closed Kan
function callAnkan(combination) {
	flag = 0 ;//replace 0 to your decision function
	if(flag > 0.5) makeCall(getOperations().an_gang);
	else declineCall(getOperations().an_gang);
}

function callShouminkan() {
	flag = 0 ;//replace 0 to your decision function
	if(flag > 0.5) makeCall(getOperations().add_gang);
	else declineCall(getOperations().add_gang);
}

function callDaiminkan() {
	flag = 0 ;//replace 0 to your decision function
	if(flag > 0.5) makeCall(getOperations().ming_gang);
	else declineCall(getOperations().ming_gang);
}

function callRon() {
	makeCall(getOperations().rong);
}

function callTsumo() {
	makeCall(getOperations().zimo);
}

function callEat() {
	flag = 0 ;//replace 0 to your decision function
	if(flag > 0.5) makeCall(getOperations().eat);
	else declineCall(getOperations().eat);
}

function callPeng() {
	flag = 0 ;//replace 0 to your decision function
	if(flag > 0.5) makeCall(getOperations().peng);
	else declineCall(getOperations().peng);
}

function canDoThirteenOrphans() {
	return false;
}

function callAbortiveDraw() { 
	if (canDoThirteenOrphans()) {
		return;
	}
	app.NetAgent.sendReq2MJ('FastTest', 'inputOperation', { type: mjcore.E_PlayOperation.jiuzhongjiupai, index: 0, timeuse: Math.random() * 2 + 1 });
	view.DesktopMgr.Inst.WhenDoOperation();
}

function getNumberOfPlayers() {
	if (!doesPlayerExist(1) || !doesPlayerExist(2) || !doesPlayerExist(3)) {
		return 3;
	}
	return 4;
}

function getCorrectPlayerNumber(player) {
	if (getNumberOfPlayers() == 4) {
		return player;
	}
	if (!doesPlayerExist(1)) {
		if (player > 0) {
			return player + 1;
		}
	}
	if (!doesPlayerExist(2)) {
		if (player > 1) {
			return player + 1;
		}
	}
	return player;
}

function getDiscardsOfPlayer(player) {
	player = getCorrectPlayerNumber(player);
	return view.DesktopMgr.Inst.players[player].container_qipai;
}

function getCallsOfPlayer(player) {
	player = getCorrectPlayerNumber(player);

	var callArray = [];
	//Mark the tiles with the player who discarded the tile
	for (let ming of view.DesktopMgr.Inst.players[player].container_ming.mings) {
		for (var i = 0; i < ming.pais.length; i++) {
			ming.pais[i].from = ming.from[i];
			if (i == 3) {
				ming.pais[i].kan = true;
			}
			else {
				ming.pais[i].kan = false;
			}
			callArray.push(ming.pais[i]);
		}
	}

	return callArray;
}

window.ownHand = [];
// var ownHand = [];

function GetHandData(mainUpdate = true) {

	dora = getDora();

	ownHand = [];
	for (let tile of getPlayerHand()) { //Get own Hand
		ownHand.push(tile.val);
		ownHand[ownHand.length - 1].valid = tile.valid; //Is valid discard
	}
	window.ownHand = ownHand;
    return ownHand;

	// discards = [];
	// for (var j = 0; j < 4; j++) { //Get Discards for all Players
	// 	var temp_discards = [];
	// 	for (var i = 0; i < getDiscardsOfPlayer(j).pais.length; i++) {
	// 		temp_discards.push(getDiscardsOfPlayer(j).pais[i].val);
	// 	}
	// 	if (getDiscardsOfPlayer(j).last_pai != null) {
	// 		temp_discards.push(getDiscardsOfPlayer(j).last_pai.val);
	// 	}
	// 	discards.push(temp_discards);
	// }
	// if (mainUpdate) {
	// 	updateDiscardedTilesSafety();
	// }

	// calls = [];
	// for (var j = 0; j < getNumberOfPlayers(); j++) { //Get Calls for all Players
	// 	calls.push(getCallsOfPlayer(j));
	// }

	// isClosed = true;
	// for (let tile of calls[0]) { //Is hand closed? Also consider closed Kans
	// 	if (tile.from != localPosition2Seat(0)) {
	// 		isClosed = false;
	// 		break;
	// 	}
	// }
	// if (tilesLeft < getTilesLeft()) { //Check if new round/reload
	// 	if (MODE === AIMODE.AUTO) {
	// 		setAutoCallWin(true);
	// 	}
	// 	strategy = STRATEGIES.GENERAL;
	// 	strategyAllowsCalls = true;
	// 	initialDiscardedTilesSafety();
	// 	riichiTiles = [null, null, null, null];
	// 	playerDiscardSafetyList = [[], [], [], []];
	// 	extendMJSoulFunctions();
	// }

	// tilesLeft = getTilesLeft();

	// if (!isDebug()) {
	// 	seatWind = getSeatWind(0);
	// 	roundWind = getRoundWind();
	// }

	// updateAvailableTiles();
}

window.GetHandData = GetHandData;



// // Get operations can do now
// function getOperations() {
// 	return mjcore.E_PlayOperation;
// }

function isSameTile(tile1, tile2, checkDora = false) {
	if (typeof tile1 == 'undefined' || typeof tile2 == 'undefined') {
		return false;
	}
	if (checkDora) {
		return tile1.index == tile2.index && tile1.type == tile2.type && tile1.dora == tile2.dora;
	}
	return tile1.index == tile2.index && tile1.type == tile2.type;
}



//Remove the given Tile from Hand
async function discardTile(ownHand, tile) {
	// log("Discard: " + getTileName(tile, false));
	console.log("Discarding: " + tile);
	for (var i = 0; i < ownHand.length; i++) {
		if (isSameTile(ownHand[i], tile, true)) {
			try {
                if (view.DesktopMgr.Inst.players[0].hand[i].valid) {
                    view.DesktopMgr.Inst.players[0]._choose_pai = view.DesktopMgr.Inst.players[0].hand[i];
                    view.DesktopMgr.Inst.players[0].DoDiscardTile();
					await sleep(1000);
					return true;
                }
            }
            catch {
                throw new Error("Cannot discard tile");
            }
		}
	}
	throw new Error("Tile not found in hand");
}

function randomInt(n) {
    return Math.floor(Math.random() * n);
}

function getDiscardTile(tiles) {
    var tile = null;
    if (tiles.length > 0) {
		n = tiles.length;
		idx = randomInt(n);
		for (var i = 0; i < n; i++) {
			t = tiles[(idx + i) % n];
			if (t.valid) {
				tile = t;
				break;
			}
		}
    }
    return tile;
}

async function discard(inputHand) {
	console.log("Discard");
	console.log(inputHand);
	var tiles = [];
    
    for (var i = 0; i < inputHand.length; i++) { //Create 13 Tile hands

        var hand = [...inputHand];
        hand.splice(i, 1);

        if (tiles.filter(t => isSameTile(t.tile, inputHand[i], true)).length > 0) { //Skip same tiles in hand
            continue;
        }

        tiles.push(inputHand[i]);
        // await new Promise(r => setTimeout(r, 10)); //Sleep a short amount of time to not completely block the browser
    }

	var tile = getDiscardTile(tiles);
    if(tile == null)
    {
        throw new Error("No tile to discard");
        return; 
    }
	
	var flag = await discardTile(inputHand, tile);
	if(flag == false)
	{
		throw new Error("Cannot discard tile");
	}
	// var riichi = false;
	// if (canRiichi()) {
	// 	tiles.sort(function (p1, p2) {
	// 		return p2.riichiPriority - p1.riichiPriority;
	// 	});
	// 	riichi = callRiichi(tiles);
	// }
	// if (!riichi) {
	// 	discardTile(tile);
	// }

	return tile;
}

window.discard = discard;

function getOperationList() {
	return view.DesktopMgr.Inst.oplist;
}

// Main loop starts here
window.Auto_run = true;
threadIsRunning = false;

//Main Loop
function main() {
	if(!window.Auto_run)
	{
		console.log("Auto_run is False");
		setTimeout(main, 500);
		return;
	}
	var operations = getOperationList();
	console.log("Main Loop"  + operations);
	if (operations == null || operations.length == 0) {	
		console.log("Waiting for own turn.");
		setTimeout(main, 500);
		return;
	}
	setTimeout(mainOwnTurn, 1000);
}

window.main = main;

async function mainOwnTurn() {
	if (threadIsRunning) {
		return;
	}
	threadIsRunning = true;

	GetHandData(); //Set current state of the board to local variables

	var operations = getOperationList();

	console.log("##### OWN TURN #####");
	
	for (let operation of operations) {
		if (getOperationList().length == 0) {
			break;
		}
		switch (operation.type) {
			case getOperations().an_gang: //From Hand
				callAnkan(operation.combination);
				break;
			case getOperations().add_gang: //Add from Hand to Pon
				callShouminkan();
				break;
			case getOperations().zimo:
				callTsumo();
				break;
			case getOperations().rong:
				callRon();
				break;
			case getOperations().jiuzhongjiupai:
				callAbortiveDraw();
				break;
		}
	}

	for (let operation of operations) {
		if (getOperationList().length == 0) {
			break;
		}
		switch (operation.type) {
			case getOperations().dapai:
				isConsideringCall = false;
				await discard(window.ownHand);
				break;
			case getOperations().eat:
				callEat();
				break;
			case getOperations().peng:
				callPeng();
				break;
			case getOperations().ming_gang: //From others
				callDaiminkan();
				break;
		}
	}

	console.log("Own turn completed.");
	threadIsRunning = false;
	setTimeout(main, 1000);
}