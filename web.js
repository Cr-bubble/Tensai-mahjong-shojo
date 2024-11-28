
function helloword() {
    console.log("Hello World");
}

window.helloword = helloword;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// MajSoul specific functions

function getDora() {
	return view.DesktopMgr.Inst.dora;
}

function getPlayerHand() {
	return view.DesktopMgr.Inst.players[0].hand;
}

function doesPlayerExist(player) {
	return typeof view.DesktopMgr.Inst.players[player].hand != 'undefined' && view.DesktopMgr.Inst.players[player].hand != null;
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
    // console.log(typeof ownHand); // 應返回 "object"
    // console.log(Array.isArray(ownHand)); // 應返回 true
    console.log(ownHand);
	window.ownHand = ownHand;
	console.log(window.ownHand);
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


function getDiscardTile(tiles) {
    var tile = null;
    if (tiles.length > 0) {
        tile = tiles[0];
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