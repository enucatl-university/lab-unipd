	implicit real*8(a-h,j,l,o-z)  
c: Apertura files
		open(1,file='dati.in',status='old')
		open(2,file='dati.out',status='new')
c: Lettura dati iniziali:
	read(1,*,err=1,end=1) xmin,xmax,ymin,ymax,cx,cy,ndiv,numit
c: definizioni variabili importanti
	cre=cx
	cim=cy
	xstep = (xmax - xmin)/dble(ndiv) 
	ystep = (ymax - ymin)/dble(ndiv) 
	nxstep = ndiv
	nystep = ndiv
c: definiamo anche il quadrato del raggio di non ritorno
	r=max(cre*cre + cim*cim, 4.d0)
c: cominciano i cicli
	do ny=0,nystep
	do nx=0,nxstep
		x=xmin+dble(nx)*xstep
		y=ymin+dble(ny)*ystep
		iter=0
		do while (((x*x+y*y).lt.r).and.(iter.le.numit)) 
 			xp=x*x - y*y + cre
			y = 2.d0*x*y + cim
			x=xp
			iter=iter+1
 		end do
 2	continue
	write(2,*) iter
	end do
	end do
 1	end

