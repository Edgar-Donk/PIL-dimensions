def make_arc_aa(dr, centre, radius, start, finish, width=1, fill=(0,0,0), back = (255,255,221)):
    xm,ym = centre
    sq = findSect((xm, ym), (start[0], start[1]))
    fq = findSect((xm, ym), (finish[0], finish[1]))
    sects = ()

    diff_sect = fq[0] - sq[0]

    if diff_sect == 0:
        sects = sq[0],fq[0]
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

    elif (diff_sect == 1) or (sq[0] == 8 and fq[0] == 1):
        sects = sq[0],0
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)
        sects = 0,fq[0]
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

    elif (diff_sect == 2) or (sq[0] == 8 and fq[0] == 2) or (sq[0] == 7 and fq[0] == 1):
        sects = sq[0],0
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)
        if sq[0] < 8:
            sects = -sq[0]-1,-sq[0]-1
        else:
            sects = -1,-1
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)
        sects = 0,fq[0]
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

    elif (diff_sect == 3) or (sq[0] == 8 and fq[0] == 3) or (sq[0] == 7 and fq[0] == 2):
        sects = sq[0],0
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

        if sq[0] < 7:
            sects = -sq[0]-2,-sq[0]-2
        else:
            sects = -1,-1
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

        if sq[0] < 8:
            sects = -sq[0]-1,-sq[0]-1
        else:
            sects = -2,-2
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)

        sects = 0,fq[0]
        PartCircleAA(dr, xm, ym, radius, start, finish, width, sects,
            fill=fill, back = back)
