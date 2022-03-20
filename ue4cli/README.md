- Game
	- Command
		- UE4Editor.exe ${Project}.uproject (exec in Project Dir, uncooked=True, Default)
		- ${Project}.exe					(exec in Project Dir, uncooked=False)

		- ${Project}.exe					(exec in Packaging Dir)

	- Params
		[${map}]

	- Options

		[-windowed -resx=${resx} -resy=${resy}
		[-log]
		[-noailogging] 
		[-NOVERIFYGC] 
		[-NOSTEAM]
		[-fullcrashdumpalways]

		-game

		-basedir = ${basedir}

- Client
	- Command
		- UE4Editor.exe ${Project}.uproject (exec in Project Dir, uncooked=True, Default)
		- ${Project}.exe					(exec in Project Dir, uncooked=False)

		- ${Project}.exe					(exec in Packaging Dir)

	- Params
		${ip} 

	- Options
		[-windowed -resx=${resx} -resy=${resy}
		[-log]
		[-noailogging] 
		[-NOVERIFYGC] 
		[-NOSTEAM]
		[-fullcrashdumpalways]

		-game


- Profile
	- Command
		- UE4Editor.exe ${Project}.uproject (exec in Project Dir, uncooked=True, Default)
		- ${Project}.exe 					(exec in Project Dir, uncooked=False)

		- ${Project}.exe					(exec in Packaging Dir)

	- Params
		[${map}] or [${ip}]

	- Options
		[-windowed -resx=${resx} -resy=${resy}
		[-log]
		[-noailogging] 
		[-NOVERIFYGC] 
		[-NOSTEAM]
		[-fullcrashdumpalways]

		-game
		-Bv.TechArt.Profile "${ProfileOptions}"

	- "${ProfileOptions}"
		phase=capture
		capturetype={video|seq}
		[targetbuffers=${buffer1}+${buffer2}+...+${bufferN}]

		phase=memory
		[dumpinterval=${interval}]

		phase=trace
		profiler={csv|stat}


- Server
	- Command
		- UE4Editor.exe ${Project}.uproject (exec in Project Dir, uncooked=True, Default)
		- ${Project}Server.exe				(exec in Project Dir, uncooked=False)

		- ${Project}Server.exe				(exec in Packaging Dir)
	- Params
		[${map}]

	- Options
		[-noailogging] 
		[-NOVERIFYGC] 
		[-NOSTEAM]
		[-fullcrashdumpalways]
		[-log]

		-server
		-game 

- Build
	- Command
		Build.bat

	- Params
		${Project}${Target}	(${Target} 			= {None|Editor|Client|Server}		)
		${Platform}			(${Platform} 		= {Win64|Win32|Mac|Linux}			)		
		${Configuration}	(${Configuration} 	= {Debug|Development|Shipping|Test}	)

	- Options
		-waitMutex
		-NoHotReload

		

- Package
	- Command
		RunUAT.bat

	- Params
		BuildCookRun

	- Options
		-project=${uproject}
		-platform={Win64|Win32|Mac|Linux}
		-clientconfig={debug|debuggame|development|shipping|test}

		[-server -serverconfig=Development -serverplatform=Win64]

		[-map=${map0}+${map2}+...${mapN}]

		[-skipstage]
		[-stage -stagingdirectory -nodebuginfo] // default directory : ../Saved/StagedBuilds

		[-archive -archivedirectoryry] // ../ArchivedBuilds

		-nop4
		-build 
		-cook 
		-compressed 
		-iterate 
		-pak
		[-bvpak]
		-fileopenlog
		-utf8output 

		-NoCompileEditor 

		-LogCmds="LogMutable Display, LogCook Display"	
